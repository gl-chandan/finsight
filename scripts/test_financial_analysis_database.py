from backend.app.repositories.financial_repository import (
    FinancialRepository
)

from backend.app.services.financial_analysis import (
    FinancialAnalysisService
)


repository = FinancialRepository()

record = repository.get_financial_record(
    company_id=1,
    fiscal_year=2025
)

if record is None:
    print("Financial record not found")
    raise SystemExit


print("Financial Record:")
print(record)


analysis = FinancialAnalysisService.analyze_record(
    record
)


print("\nFinancial Analysis:")
print(analysis)