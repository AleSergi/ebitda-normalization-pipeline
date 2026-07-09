import requests

# CONFIGURAZIONE CENTRALE
# Cambia solo questo valore per analizzare un'altra azienda
TICKER = "AAPL"

HEADERS = {'User-Agent': 'Alessandro Sergi alessandrosergi85@gmail.com'}


def get_cik_from_ticker(ticker):
    url = "https://www.sec.gov/files/company_tickers.json"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    for key, company in data.items():
        if company['ticker'] == ticker.upper():
            return str(company['cik_str']).zfill(10)
    raise ValueError(f"Ticker {ticker} non trovato.")


def get_latest_fact(cik, concept_name):
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    facts = response.json()
    try:
        concept_data = facts['facts']['us-gaap'][concept_name]
        units = concept_data['units']['USD']
        annual_data = [item for item in units if item.get('form') in ['10-K', '10-K/A']]
        annual_data_sorted = sorted(annual_data, key=lambda x: (x.get('fy', 0), x.get('end', '')), reverse=True)
        latest_record = annual_data_sorted[0]
        return {"year": latest_record['fy'], "end_date": latest_record['end'], "value": latest_record['val']}
    except KeyError:
        return None


def get_unadjusted_ebitda(ticker):
    """Calcola l'EBITDA base matematico."""
    cik = get_cik_from_ticker(ticker)
    tags = {
        "Net Income": "NetIncomeLoss",
        "Taxes": "IncomeTaxExpenseBenefit",
        "Interest Expense": "InterestExpense",
        "D&A": "DepreciationAndAmortization"
    }
    financials = {}
    target_year, target_end_date = None, None
    for label, tag in tags.items():
        data = get_latest_fact(cik, tag)
        if data:
            financials[label] = data['value']
            if label == "Net Income":
                target_year, target_end_date = data['year'], data['end_date']
        else:
            financials[label] = 0

    unadjusted_ebitda = sum(financials.values())
    return {"year": target_year, "end": target_end_date, "components": financials, "total": unadjusted_ebitda}


def debug_financials(ticker):
    """Funzione di Audit per verificare i dati estratti."""
    print(f"--- AUDIT XBRL PER {ticker} ---")
    data = get_unadjusted_ebitda(ticker)
    if data:
        for key, value in data['components'].items():
            print(f" > {key}: {value / 1_000_000_000:,.2f} Mld")
        print("-" * 30)
        print(f"UNADJUSTED EBITDA: {data['total'] / 1_000_000_000:,.2f} Mld")


if __name__ == "__main__":
    # Esecuzione sequenziale: Audit seguito dal calcolo
    debug_financials(TICKER)