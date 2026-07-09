from sec_edgar_downloader import Downloader

def download_10k(ticker, company = "Alessandro Sergi", email = "alessandrosergi85@gmail.com") -> str:
    dl = Downloader(company, email)
    # limit=1 scarica solo l'ultimo. download_details=True scarica i file HTML puliti
    dl.get("10-K", ticker, limit=1, download_details=True)

    print(f"[*] Download completato. File salvati in: sec-edgar-filings/{ticker}/10-K")

    if __name__ == "__main__":
        download_10k(ticker)