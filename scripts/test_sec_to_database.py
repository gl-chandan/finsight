from backend.app.services.sec_client import SECClient
from backend.app.ingestion.financial_loader import (
    FinancialDataLoader,
    validate_financial_record
)
from backend.app.repositories.financial_repository import (
    FinancialRepository
)


# ==========================================================
# 1. SEC Client
# ==========================================================

client = SECClient(
    user_agent="FinSight proninja314@gmail.com"
)


# ==========================================================
# 2. Financial Loader
# ==========================================================

loader = FinancialDataLoader(client)


# ==========================================================
# 3. Financial Repository
# ==========================================================

repository = FinancialRepository()


# ==========================================================
# 4. Load NVIDIA financial data
# ==========================================================

years = [2024, 2025]


for fiscal_year in years:

    print("\n" + "=" * 60)

    print(
        f"Loading NVIDIA FY{fiscal_year}..."
    )

    # ------------------------------------------------------
    # Create financial record
    # ------------------------------------------------------

    record = loader.create_financial_record(
        company_id=1,
        fiscal_year=fiscal_year,
        cik="0001045810"
    )

    # ------------------------------------------------------
    # Validate
    # ------------------------------------------------------

    validate_financial_record(record)

    print("\nFinancial record:")
    print(record)

    # ------------------------------------------------------
    # Save to PostgreSQL
    # ------------------------------------------------------

    financial_period_id = (
        repository.save_financial_record(
            record
        )
    )

    print(
        f"\nSuccessfully saved FY{fiscal_year}."
    )

    print(
        f"Financial Period ID: "
        f"{financial_period_id}"
    )


print("\n" + "=" * 60)

print("Finished loading financial data.")