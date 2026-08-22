CREATE TABLE companies (
    id SERIAL PRIMARY KEY,

    name VARCHAR(255) NOT NULL,

    ticker VARCHAR(20) NOT NULL UNIQUE,

    cik VARCHAR(20) UNIQUE,

    industry VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE financial_periods (
    id SERIAL PRIMARY KEY,

    company_id INTEGER NOT NULL,

    fiscal_year INTEGER NOT NULL,

    period_type VARCHAR(10) NOT NULL,

    start_date DATE,

    end_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_company
        FOREIGN KEY (company_id)
        REFERENCES companies(id),

    CONSTRAINT unique_company_period
        UNIQUE (
            company_id,
            fiscal_year,
            period_type
        )
);

CREATE TABLE income_statements (
    id SERIAL PRIMARY KEY,

    financial_period_id INTEGER NOT NULL UNIQUE,

    revenue NUMERIC(20, 2),

    cost_of_revenue NUMERIC(20, 2),

    gross_profit NUMERIC(20, 2),

    operating_income NUMERIC(20, 2),

    net_income NUMERIC(20, 2),

    FOREIGN KEY (financial_period_id)
        REFERENCES financial_periods(id)
);

CREATE TABLE balance_sheets (
    id SERIAL PRIMARY KEY,

    financial_period_id INTEGER NOT NULL UNIQUE,

    cash NUMERIC(20, 2),

    total_assets NUMERIC(20, 2),

    total_liabilities NUMERIC(20, 2),

    total_debt NUMERIC(20, 2),

    equity NUMERIC(20, 2),

    FOREIGN KEY (financial_period_id)
        REFERENCES financial_periods(id)
);

CREATE TABLE cash_flow_statements (
    id SERIAL PRIMARY KEY,

    financial_period_id INTEGER NOT NULL UNIQUE,

    operating_cash_flow NUMERIC(20, 2),

    capital_expenditure NUMERIC(20, 2),

    free_cash_flow NUMERIC(20, 2),

    FOREIGN KEY (financial_period_id)
        REFERENCES financial_periods(id)
);

