from app.ingestion.financial_loader import get_annual_value


values = [
    {
        "value": 100,
        "fiscal_year": 2025,
        "fiscal_period": "Q1"
    },
    {
        "value": 200,
        "fiscal_year": 2025,
        "fiscal_period": "Q2"
    },
    {
        "value": 300,
        "fiscal_year": 2025,
        "fiscal_period": "FY"
    }
]


result = get_annual_value(
    values,
    2025
)

print(result)