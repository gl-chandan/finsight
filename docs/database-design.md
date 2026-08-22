# FinSight Database

## Database

PostgreSQL

## Main Tables

- companies
- financial_periods
- income_statements
- balance_sheets
- cash_flow_statements

## Relationships

companies
    |
    | 1:N
    v
financial_periods
    |
    +---- income_statements
    |
    +---- balance_sheets
    |
    +---- cash_flow_statements

## Financial Metrics

Derived metrics include:

- Operating Margin
- Net Margin
- Debt-to-Equity
- Free Cash Flow