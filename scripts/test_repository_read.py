from backend.app.repositories.financial_repository import (
    FinancialRepository
)


repository = FinancialRepository()

record = repository.get_financial_record(
    company_id=1,
    fiscal_year=2025
)

print(record)