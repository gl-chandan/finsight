from backend.app.agents.financial_agent import (
    FinancialAgent
)

from backend.app.repositories.financial_repository import (
    FinancialRepository
)


repository = FinancialRepository()

agent = FinancialAgent(
    repository=repository
)


result = agent.get_financial_data(
    company_id=1,
    fiscal_year=2025
)


print("\n" + "=" * 60)

print("FINANCIAL AGENT TEST")

print("=" * 60)


if result is None:

    print("No financial data found.")

else:

    record = result["financial_record"]

    metrics = result["calculated_metrics"]

    print("\nRevenue:")
    print(record.revenue)

    print("\nNet Income:")
    print(record.net_income)

    print("\nROA:")
    print(metrics["return_on_assets"])

    print("\nROE:")
    print(metrics["return_on_equity"])

    print("\nNet Margin:")
    print(metrics["net_margin"])