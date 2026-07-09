import os
from dotenv import load_dotenv
import xbrl_fetcher
import nlp_engine
import exporter
import parser

# Carica le variabili d'ambiente dal file .env (API Key)
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# CONFIGURAZIONE CENTRALE

def main(ticker):
    print(f"=== AVVIO PIPELINE AUTOMATIZZATA DI QoE: {ticker} ===")

    # PHASE 1: Estrazione Dati Contabili Certificati (XBRL)
    # Interroga il database della SEC per ricostruire la base matematica
    base_financials = xbrl_fetcher.get_unadjusted_ebitda(ticker)
    if not base_financials:
        print("[!] Errore Critico: Impossibile recuperare la base quantitativa XBRL. Arresto pipeline.")
        return

    # PHASE 2: Parsing Narrativo ed Estrazione Semantica (AI Layer)
    # Qui richiami le funzioni che avevi implementato per scaricare il 10-K e analizzarlo
    print("\n[2/4] Isolamento testo della sezione MD&A (Item 7)...")
    target_folder = f"sec-edgar-filings/{ticker}/10-K"

    try:
        # Usa il parser corretto pasando la cartella
        raw_mda_text = parser.extract_item_7(target_folder)
    except FileNotFoundError as e:
        print(f"[!] Errore: {e}")
        print("Assicurati di aver prima scaricato il bilancio SEC nella cartella corretta.")
        return

    print("\n[3/4] Analisi semantica One-off ed esecuzione Audit AI...")
    adjustments_pydantic = nlp_engine.extract_adjustments(raw_mda_text, ANTHROPIC_API_KEY)
    if hasattr(adjustments_pydantic, 'dict'):
        adjustments_json = adjustments_pydantic.model_dump().get('adjustments', [])
    else:
        adjustments_json = adjustments_pydantic  # Fallback

    # 2. Generazione Audit (usando il nome esatto e l'ordine esatto dei parametri)
    audit_memo_response = nlp_engine.audit_adjustments(raw_mda_text, adjustments_json, ANTHROPIC_API_KEY)

    # Estraiamo il testo della risposta di Claude
    audit_memo = getattr(audit_memo_response, 'content', str(audit_memo_response))

    # PHASE 3: Triangolazione e Consolidamento dei Dati
    print("\n[4/4] Consolidamento della struttura dati unificata...")
    unadjusted_ebitda_val = base_financials["total"]

    # Struttura dati finale (Master Dictionary) che verrà passata all'exporter
    consolidated_data = {
        "ticker": ticker,
        "year": base_financials["year"],
        "end_date": base_financials["end"],
        "quantitative_base": base_financials["components"],
        "unadjusted_ebitda": unadjusted_ebitda_val,
        "adjustments": adjustments_json,
        "audit_report": audit_memo
    }

    # Output di controllo a terminale
    print("\n=================== SINTESI PIPELINE MAIN ===================")
    print(f"Asset Target          : {ticker}")
    print(f"Esercizio Fiscale     : {consolidated_data['year']} (Chiusura: {consolidated_data['end_date']})")
    print(f"Net Income di base    : $ {consolidated_data['quantitative_base']['Net Income'] / 1_000_000_000:.2f} Mld")
    print(f"UNADJUSTED EBITDA BASE: $ {consolidated_data['unadjusted_ebitda'] / 1_000_000_000:.2f} Mld")
    print("=============================================================")

    print("\n[Successo] Main orchestrator configurato.")

    # PHASE 4: Generazione dei Deliverables Finanziari
    print("\n[Exporter] Avvio esportazione modelli finanziari...")

    # Definiamo il nome del file dinamico basato sul ticker selezionato
    excel_filename = f"EBITDA_Bridge_{ticker}.xlsx"
    exporter.create_ebitda_bridge_excel(consolidated_data, filename=excel_filename)

    print("\n=================== PIPELINE COMPLETATA CON SUCCESSO ===================")
    print(f"1. Base Quantitativa Calcolata (SEC XBRL)")
    print(f"2. Analisi Semantica & One-off Isolate (Claude AI Layer)")
    print(f"3. Audit Report Generato e Validato (Audit_Report_{ticker}.md)")
    print(f"4. Excel EBITDA Bridge Generato con Formule Native ({excel_filename})")
    print("=========================================================================")

    return consolidated_data


if __name__ == "__main__":
    main()