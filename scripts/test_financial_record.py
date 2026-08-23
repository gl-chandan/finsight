from app.ingestion.financial_loader import FinancialDataLoader
from app.services.sec_client import SECClient


client = SECClient(
    user_agent="FinSight proninja314@gmail.com"
)

loader = FinancialDataLoader(client)

record = loader.create_financial_record(
    company_id=1,
    fiscal_year=2025,
    cik="0001045810"
)

print(record)