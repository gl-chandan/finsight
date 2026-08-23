from app.ingestion.financial_loader import FinancialDataLoader
from app.services.sec_client import SECClient


client = SECClient(
    user_agent="FinSight proninja314@gmail.com"
)

loader = FinancialDataLoader(client)

data = loader.load_company_facts(
    "0001045810",
    2025
)

for key, value in data.items():
    print(f"\n{key}:")
    print(value)