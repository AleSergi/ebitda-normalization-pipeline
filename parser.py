import os
import re
from bs4 import BeautifulSoup


def extract_item_7(folder_path: str) -> str:
    target_file = None

    # 1A. Ricerca primaria: File HTML pulito
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith((".htm", ".html")):
                target_file = os.path.join(root, file)
                break
        if target_file: break

    # 1B. Fallback: File di testo grezzo
    if not target_file:
        for root, dirs, files in os.walk(folder_path):
            if "full-submission.txt" in files:
                target_file = os.path.join(root, "full-submission.txt")
                break

    if not target_file:
        raise FileNotFoundError(f"Errore: Nessun bilancio scaricato in {folder_path}")

    # 2. Lettura del file
    with open(target_file, 'r', encoding='utf-8') as file:
        raw_text = file.read()

    # 3. Pulizia d'emergenza (rimuove l'header SGML se presente)
    start_pos = raw_text.find("<DOCUMENT>")
    if start_pos != -1:
        raw_text = raw_text[start_pos:]

    # 4. Appiattimento dei tag HTML con BeautifulSoup
    soup = BeautifulSoup(raw_text, "html.parser")
    clean_text = soup.get_text(separator=' ', strip=True)

    # 5. Estrazione logica (Ricerca multipla per bypassare l'Indice)
    pattern = re.compile(
        r"(item\s*7\.\s*management['’]s\s*discussion.*?)(item\s*8\.)",
        re.IGNORECASE | re.DOTALL
    )

    # finditer trova TUTTE le occorrenze, non si ferma alla prima
    matches = pattern.finditer(clean_text)

    extracted_text = ""
    for match in matches:
        text_found = match.group(1).strip()
        # Teniamo solo il match più lungo (il capitolo vero, non l'indice)
        if len(text_found) > len(extracted_text):
            extracted_text = text_found

    # Un vero MD&A è lungo almeno qualche migliaio di caratteri
    if extracted_text and len(extracted_text) > 2000:
        print(f"      Successo: Estratti {len(extracted_text)} caratteri utili (Capitolo trovato).")
        return extracted_text
    else:
        raise ValueError(
            f"Parser fallito: Trovati solo {len(extracted_text)} caratteri. Probabilmente ha letto solo l'indice.")