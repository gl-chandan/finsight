INSERT INTO companies
(name, ticker, cik, industry)
VALUES
('NVIDIA', 'NVDA', '0001045810', 'Semiconductors'),
('Microsoft', 'MSFT', '0000789019', 'Technology'),
('Apple', 'AAPL', '0000320193', 'Technology');

INSERT INTO financial_periods
(company_id, fiscal_year, period_type)
VALUES
(1, 2025, 'FY'),
(2, 2025, 'FY'),
(3, 2025, 'FY');

INSERT INTO income_statements
(
    financial_period_id,
    revenue,
    cost_of_revenue,
    gross_profit,
    operating_income,
    net_income
)
VALUES
(1, 130000, 30000, 100000, 80000, 72000),
(2, 250000, 80000, 170000, 110000, 90000),
(3, 400000, 220000, 180000, 120000, 100000);


INSERT INTO balance_sheets
(
    financial_period_id,
    cash,
    total_assets,
    total_liabilities,
    total_debt,
    equity
)
VALUES
(1, 50000, 100000, 40000, 20000, 60000),
(2, 80000, 300000, 150000, 60000, 150000),
(3, 70000, 350000, 180000, 100000, 170000);

INSERT INTO cash_flow_statements
(
    financial_period_id,
    operating_cash_flow,
    capital_expenditure,
    free_cash_flow
)
VALUES
(1, 70000, 10000, 60000),
(2, 100000, 20000, 80000),
(3, 110000, 15000, 95000);

