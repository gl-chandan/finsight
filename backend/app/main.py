from app.models.company import Company

from app.models.financial_statement import (
    IncomeStatement,
    BalanceSheet,
    CashFlowStatement
)

from app.services.financial_analysis import (
    FinancialAnalysisService
)


company = Company(
    name="NVIDIA",
    ticker="NVDA",
    cik="0001045810",
    industry="Semiconductors"
)

income_statement = IncomeStatement(
    fiscal_year=2025,
    revenue=130,
    cost_of_revenue=30,
    operating_income=80,
    net_income=72
)

balance_sheet = BalanceSheet(
    fiscal_year=2025,
    cash=50,
    total_assets=100,
    total_liabilities=40,
    total_debt=20,
    equity=60
)

cash_flow = CashFlowStatement(
    fiscal_year=2025,
    operating_cash_flow=70,
    capital_expenditure=10
)


print(company)
print()

print("FY2025")
print("-------")

print(
    "Income Metrics:",
    income_statement.calculate_metrics()
)

print(
    "Balance Metrics:",
    balance_sheet.calculate_metrics()
)

print(
    "Cash Flow Metrics:",
    cash_flow.calculate_metrics()
)

growth = FinancialAnalysisService.calculate_growth(
    current=130,
    previous=100
)

print(
    f"Revenue Growth: {growth:.2f}%"
)