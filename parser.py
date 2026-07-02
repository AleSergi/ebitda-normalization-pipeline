import os
import re
from bs4 import BeautifulSoup


def extract_item_7(folder_path: str) -> str:
    """
    Legge il file 10-K dalla cartella specificata, pulisce i tag HTML
    ed estrae esclusivamente la sezione Item 7 (MD&A) tramite Regex.
    """
    # Trova il file del documento (solitamente con estensione .txt o .htm)
    file_name = os.listdir(folder_path)[0]
    file_path = os.path.join(folder_path, file_name, "full-submission.txt")

    # Apre il file in modalità lettura gestendo l'encoding
    with open(file_path, 'r', encoding='utf-8') as file:
        raw_html = file.read()

    # Parsing dell'HTML tramite BeautifulSoup per estrarre solo il testo (ignora tabelle/immagini complesse)
    soup = BeautifulSoup(raw_html, "html.parser")
    clean_text = soup.get_text(separator=' ', strip=True)

    # Compilazione dei pattern Regex per trovare l'inizio di Item 7 e l'inizio di Item 8
    # re.IGNORECASE permette di intercettare variazioni di maiuscole/minuscole
    pattern_start = re.compile(r"Item\s+7\.\s+Management['’]s\s+Discussion\s+and\s+Analysis", re.IGNORECASE)
    pattern_end = re.compile(r"Item\s+8\.\s+Financial\s+Statements\s+and\s+Supplementary\s+Data", re.IGNORECASE)

    # Ricerca delle corrispondenze all'interno della stringa pulita
    match_start = pattern_start.search(clean_text)
    match_end = pattern_end.search(clean_text)

    # Se i pattern non vengono trovati, solleva un'eccezione
    if not match_start or not match_end:
        raise ValueError("Impossibile individuare i delimitatori Item 7 o Item 8 nel testo.")

    # Slicing della stringa per isolare il testo compreso tra i due match
    item_7_text = clean_text[match_start.end():match_end.start()].strip()

    return item_7_text