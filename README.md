# Quality of Earnings (QoE) Automator

## Executive Summary
As a finance student with a strong interest in Investment Banking and M&A advisory, I developed this independent project to address a common inefficiency in financial modeling: the manual normalization of EBITDA. During Quality of Earnings (QoE) analysis, analysts spend hours reading through a company's Form 10-K, specifically the Management's Discussion and Analysis (MD&A), to identify non-recurring items. 
This project is an automated ETL (Extract, Transform, Load) pipeline that streamlines this process. It extracts certified quantitative data via SEC APIs and leverages Large Language Models (LLMs) to perform a semantic audit of the text. The final output is an audit-ready, interactive EBITDA Bridge exported directly into Excel.

## Financial Methodology
The tool is designed to replicate the analytical framework of a financial analyst, structured across three main phases:

**1. Quantitative Baseline (SEC EDGAR API)**
The pipeline first establishes a mathematical baseline by querying the SEC EDGAR XBRL databases. It extracts pure US-GAAP figures, including Net Income, Provision for Income Taxes, Interest Expense, and Depreciation & Amortization (D&A), to calculate the Unadjusted EBITDA. This ensures the foundation of the model relies solely on certified accounting data rather than AI-generated estimates.

**2. Semantic Audit (NLP via Anthropic Claude 3)**
Once the baseline is established, the tool extracts the Item 7 (MD&A) section from the Form 10-K. Using financial prompt engineering, the LLM isolates one-off items and assigns the correct algebraic polarity based on their economic nature. For instance, costs and losses (e.g., legal settlements, restructuring costs) are classified as positive add-backs, while non-operating benefits (e.g., unrealized equity gains, asset sales) are classified as negative deductions.

**3. Financial Reporting**
The integrated data is then exported into a professionally formatted Excel spreadsheet. Rather than hardcoding the final values, the script injects native Excel formulas (such as SUM functions) into the cells. This ensures that the resulting EBITDA Bridge remains fully interactive, allowing analysts to perform subsequent stress tests and manual adjustments without breaking the model's logic.

## Case Studies and Validation
The algorithm has been backtested on complex corporate filings to ensure it correctly identifies and polarizes extraordinary items. The full output files are available in the `/reports` directory.
Notable test cases include:
* **Amazon (AMZN) FY25:** The semantic engine successfully isolated a $2.5 billion FTC lawsuit settlement as an add-back, while accurately identifying a $15.2 billion unrealized gain on the Anthropic equity investment as a deduction, preventing an artificial inflation of the operating cash flow proxies.
* **Apple (AAPL) FY25:** The tool identified and normalized a $10.7 billion non-recurring tax impact related to the State Aid Decision.

## Technical Architecture
The pipeline is built entirely in Python, utilizing the following stack:
* **Data Ingestion:** `sec-edgar-downloader` for automated scraping and local archiving of SEC filings.
* **Data Processing:** `BeautifulSoup4` and Regular Expressions for HTML parsing and surgical extraction of the Item 7 section.
* **LLM Orchestration:** `Anthropic API` combined with `Pydantic` to enforce a strict JSON output structure, preventing hallucinations and ensuring data integrity.
* **Exporting:** `OpenPyXL` for generating the dynamic financial report.

## Future Roadmap
To further align this tool with institutional standards, I am currently exploring the following technical improvements:
* **Dynamic Materiality Threshold:** Implementing a percentage-based filter linked to the Unadjusted EBITDA. This will instruct the AI to ignore economically immaterial adjustments, reducing noise in the final bridge.
* **Retrieval-Augmented Generation (RAG) on Item 8:** Developing a vector database architecture to cross-reference the management's narrative in Item 7 with the granular forensic data buried in the Financial Notes (Item 8), further improving the accuracy of the semantic audit.

---
*Disclaimer: This project was developed solely for academic and portfolio purposes. The data and models generated do not constitute financial advice, investment recommendations, or professional advisory services.*