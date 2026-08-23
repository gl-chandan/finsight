from backend.app.services.sec_client import SECClient
from backend.app.ingestion.financial_loader import (
    FinancialDataLoader,
    validate_financial_record
)
from backend.app.repositories.financial_repository import (
    FinancialRepository
)


# 1. SEC Client
client = SECClient(
    user_agent="FinSight proninja314@gmail.com"
)


# 2. Financial Loader
loader = FinancialDataLoader(client)


# 3. Load NVIDIA FY2025 data
record = loader.create_financial_record(
    company_id=1,
    fiscal_year=2025,
    cik="0001045810"
)


# 4. Validate
validate_financial_record(record)

print("Financial record:")
print(record)


# 5. Save to PostgreSQL
repository = FinancialRepository()

financial_period_id = repository.save_financial_record(
    record
)


print(
    f"Successfully saved financial data."
)

print(
    f"Financial Period ID: {financial_period_id}"
)