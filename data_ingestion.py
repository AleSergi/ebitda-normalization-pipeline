import os
from sec_edgar_downloader import Downloader


def download_10k(ticker: str, user_company: str, user_email: str) -> str:
    """
    Scarica l'ultimo modulo 10-K per il ticker specificato.
    Ritorna il percorso assoluto della cartella di download.
    """
    # Inizializza l'oggetto Downloader con i parametri di identificazione richiesti dalla SEC
    dl = Downloader(user_company, user_email)

    # Esegue la GET request limitata al documento più recente (limit=1)
    try:
        dl.get("10-K", ticker, limit=1)
    except Exception as e:
        raise RuntimeError(f"Errore di rete o API durante il download: {e}")

    # Costruisce il path relativo standard generato dalla libreria
    download_folder = os.path.join(os.getcwd(), "sec-edgar-filings", ticker, "10-K")

    # Verifica che la directory esista e contenga file
    if not os.path.exists(download_folder):
        raise FileNotFoundError(f"Directory non trovata: {download_folder}")

    return download_folder