from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# Definizione dello schema Pydantic per forzare l'output JSON strutturato
class Adjustment(BaseModel):
    adjustment_type: str = Field(description="Tipo di aggiustamento (es. Restructuring, Impairment)")
    amount_millions: float = Field(description="Importo in milioni di dollari (usa valori assoluti positivi)")
    justification: str = Field(description="Frase esatta dal testo che giustifica l'aggiustamento")

class EBITDA_Adjustments(BaseModel):
    adjustments: list[Adjustment] = Field(description="Lista degli aggiustamenti straordinari trovati")


def extract_adjustments(mda_text: str, openai_api_key: str) -> dict:
    """
    Invia il testo estratto all'LLM e ritorna un dizionario contenente
    gli aggiustamenti estratti e formattati secondo lo schema Pydantic.
    """
    # Inizializza il parser associandolo allo schema definito
    parser = PydanticOutputParser(pydantic_object=EBITDA_Adjustments)

    # Configurazione del modello (GPT-4o mini usato per bilanciare costi/performance)
    llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini", api_key=openai_api_key)

    # Definizione del prompt con iniezione dinamica delle istruzioni di formattazione
    prompt = PromptTemplate(
        template="""Sei un algoritmo di estrazione dati finanziari.
        Analizza il seguente testo tratto dall'Item 7 di un modulo 10-K.
        Trova ed estrai ESCLUSIVAMENTE le spese o i ricavi NON RICORRENTI (one-off items).
        Ignora le spese operative standard (COGS, SG&A, R&D).

        {format_instructions}

        Testo da analizzare:
        {text}
        """,
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # Chain di esecuzione: Prompt -> LLM -> Parser Pydantic
    chain = prompt | llm | parser

    # Esecuzione della chain sul testo di input (limitiamo il testo a 30k char per sicurezza token)
    response = chain.invoke({"text": mda_text[:30000]})

    # Ritorna l'oggetto parsato come dizionario nativo Python
    return response.dict()