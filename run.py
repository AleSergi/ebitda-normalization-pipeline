import data_ingestion
import main

ticker = "PFE"

def run_pipeline(ticker):
    print(f"--- Inizio Pipeline Completa per {ticker} ---")
    data_ingestion.download_10k(ticker) # Assicurati che la tua funzione si chiami così
    main.main(ticker) # Assicurati di passare il ticker al main se necessario
    print(f"--- Pipeline completata per {ticker} ---")

if __name__ == "__main__":
    run_pipeline(ticker)