import pandas as pd


def create_excel_report(data_dict: dict, ticker: str) -> str:
    """
    Converte il dizionario degli aggiustamenti in un DataFrame Pandas
    e lo esporta in formato .xlsx.
    """
    # Estrazione della lista di dizionari dalla chiave radice
    adjustments_list = data_dict.get("adjustments", [])

    # Se non ci sono aggiustamenti, crea un DataFrame vuoto con le colonne definite
    if not adjustments_list:
        df = pd.DataFrame(columns=["Ticker", "Adjustment Type", "Amount (Millions $)", "Source Text"])
    else:
        # Costruzione del DataFrame Pandas
        df = pd.DataFrame(adjustments_list)
        # Rinomina le colonne per la visualizzazione finale
        df = df.rename(columns={
            "adjustment_type": "Adjustment Type",
            "amount_millions": "Amount (Millions $)",
            "justification": "Source Text"
        })
        # Aggiunta di una colonna statica per il Ticker dell'azienda
        df.insert(0, "Ticker", ticker.upper())

        # Calcolo del totale (sommatoria degli aggiustamenti) e inserimento come riga finale
        total_adjustments = df["Amount (Millions $)"].sum()
        total_row = pd.DataFrame([{
            "Ticker": "TOTAL",
            "Adjustment Type": "Total Normalization",
            "Amount (Millions $)": total_adjustments,
            "Source Text": "-"
        }])
        df = pd.concat([df, total_row], ignore_index=True)

    # Salvataggio del DataFrame in file Excel
    output_filename = f"{ticker}_EBITDA_Adjustments.xlsx"
    df.to_excel(output_filename, index=False, engine='openpyxl')

    return output_filename