from backend.app.db.connection import get_connection


def test_database_connection():
    connection = get_connection()

    assert connection is not None

    connection.close()

from backend.app.repositories.financial_repository import (
    FinancialRepository
)


def test_get_financial_record():

    repository = FinancialRepository()

    record = repository.get_financial_record(
        company_id=1,
        fiscal_year=2025
    )

    assert record is not None

    assert record.company_id == 1
    assert record.fiscal_year == 2025

    assert record.revenue is not None
    assert record.net_income is not None
    assert record.assets is not None
    assert record.equity is not None
    assert record.cash is not None