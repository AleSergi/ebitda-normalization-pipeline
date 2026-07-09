import os
from dotenv import load_dotenv
from anthropic import Anthropic


def list_available_models():
    # 1. Carica la chiave dal tuo file .env
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print("❌ ERRORE: Nessuna API Key trovata. Controlla il file .env")
        return

    print("🔄 Interrogazione dei server Anthropic in corso...")

    try:
        # 2. Inizializza il client ufficiale
        client = Anthropic(api_key=api_key)

        # 3. Richiede la lista dei modelli accessibili per questo account
        models = client.models.list()

        print("\n✅ Connessione Riuscita! Ecco i modelli esatti che PUOI usare:")
        print("-" * 50)

        # 4. Stampa gli ID esatti da copiare nel tuo nlp_engine.py
        for model in models.data:
            print(f"- {model.id}")

        print("-" * 50)
        print("💡 Copia uno di questi ID esatti e incollalo in nlp_engine.py alla voce 'model='")

    except Exception as e:
        print(f"\n❌ ERRORE DI CONNESSIONE O PERMESSI: {e}")
        print("Se vedi un errore 401 o 403, la chiave è sbagliata o il credito non è attivo.")


if __name__ == "__main__":
    list_available_models()