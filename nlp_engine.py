from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


# Definizione dello standard di Output (Compliance Bancaria)
class Adjustment(BaseModel):
    adjustment_type: str = Field(description="Tipo di costo/ricavo non ricorrente (es. Restructuring, Impairment)")
    amount_millions: float = Field(description="Importo in milioni di dollari (usa valori assoluti positivi)")
    justification: str = Field(description="Frase esatta dal testo che giustifica l'aggiustamento")


class EBITDA_Adjustments(BaseModel):
    adjustments: list[Adjustment] = Field(description="Lista degli aggiustamenti straordinari")


def extract_adjustments(text: str, api_key: str):
    # Inizializzazione di Claude
    llm = ChatAnthropic(
        model="claude-sonnet-5",
        api_key=api_key,
    )

    parser = PydanticOutputParser(pydantic_object=EBITDA_Adjustments)

    prompt = PromptTemplate(
        template="""Agisci come un Analista M&A esperto in Quality of Earnings. 
    Analizza la sezione Item 7 (MD&A) e isola solo le voci non ricorrenti (One-Off).

    REGOLE SUI SEGNI ALGEBRICI (CRITICO):
    Analizza la natura economica di ogni voce e applica rigorosamente questo segno algebrico:
    1. Se la voce è un COSTO, PERDITA o SPESA (es. svalutazioni, severance, cause legali, restructuring), restituisci il valore come POSITIVO (es. 2500), perché va sommato (Add-back) per normalizzare l'EBITDA.
    2. Se la voce è un RICAVO, GUADAGNO o BENEFICIO (es. equity investment gain, sale of asset, tax benefit), restituisci il valore come NEGATIVO (es. -15200), perché va sottratto dall'EBITDA.

    {format_instructions}

    Testo del bilancio:
    {text}""",
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser

    # Invio testo (tagliamo a 80k caratteri di sicurezza per evitare token overflow)
    return chain.invoke({"text": text[:80000]})


def audit_adjustments(text, adjustments_json, api_key):
    llm = ChatAnthropic(model="claude-sonnet-5", api_key=api_key)

    prompt = f"""
    Sei un Senior Auditor.
    Testo originale MD&A: {text[:50000]}
    Dati estratti dal parser: {adjustments_json}

    Verifica: gli importi estratti sono presenti nel testo? La giustificazione è corretta?
    Rispondi con un report di validazione in formato Markdown.
    """
    return llm.invoke(prompt)