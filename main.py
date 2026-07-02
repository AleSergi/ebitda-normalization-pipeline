import os
from dotenv import load_dotenv
from data_ingestion import download_10k
from parser import extract_item_7
from nlp_engine import extract_adjustments
from exporter import create_excel_report


def main():
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("API Key non trovata.")

    # 1. Configurazione Parametri (Hardcoded per il test, in prod andrebbero in un file .env)
    TICKER = "AAPL"
    USER_COMPANY = "PortfolioProject_AleSergi"
    USER_EMAIL = "alessandrosergi85@gmail.com"

    print(f"--- Inizio Pipeline Estrazione EBITDA Normalizzato per {TICKER} ---")

    try:
        # Modulo 1: Ingestion
        print("[1/4] Download del Form 10-K da SEC EDGAR...")
        folder_path = download_10k(TICKER, USER_COMPANY, USER_EMAIL)

        # Modulo 2: Parsing
        print("[2/4] Estrazione della sezione Item 7 (MD&A)...")
        item_7_text = extract_item_7(folder_path)
        print(f"      Estratti {len(item_7_text)} caratteri utili.")

        # Modulo 3: NLP
        print("[3/4] Analisi semantica LLM in corso (Ricerca One-Off Items)...")
        json_data = extract_adjustments(item_7_text, OPENAI_API_KEY)

        # Modulo 4: Export
        print("[4/4] Generazione Audit Report in Excel...")
        excel_file = create_excel_report(json_data, TICKER)

        print(f"--- Pipeline Completata con Successo! ---")
        print(f"Report salvato in: {excel_file}")

    except Exception as e:
        print(f"ERRORE CRITICO NELLA PIPELINE: {e}")


if __name__ == "__main__":
    main()