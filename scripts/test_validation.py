from app.ingestion.financial_loader import (
    FinancialRecord,
    validate_financial_record
)


record = FinancialRecord(
    company_id=1,
    fiscal_year=2025,
    revenue=1000,
    net_income=200,
    assets=5000,
    liabilities=2000,
    equity=3000,
    cash=1000,
    operating_cash_flow=500
)

result = validate_financial_record(record)

print("Validation result:", result)