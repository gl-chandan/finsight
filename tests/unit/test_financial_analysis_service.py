import pytest

from backend.app.services.financial_analysis import (
    FinancialAnalysisService
)


service = FinancialAnalysisService()


def test_operating_margin():

    result = service.calculate_operating_margin(
        operating_income=20,
        revenue=100
    )

    assert result == 20.0


def test_net_margin():

    result = service.calculate_net_margin(
        net_income=10,
        revenue=100
    )

    assert result == 10.0


def test_debt_to_equity():

    result = service.calculate_debt_to_equity(
        total_debt=50,
        equity=100
    )

    assert result == 0.5


def test_free_cash_flow():

    result = service.calculate_free_cash_flow(
        operating_cash_flow=100,
        capital_expenditure=30
    )

    assert result == 70


def test_operating_margin_zero_revenue():

    with pytest.raises(ValueError):

        service.calculate_operating_margin(
            operating_income=20,
            revenue=0
        )


def test_net_margin_zero_revenue():

    with pytest.raises(ValueError):

        service.calculate_net_margin(
            net_income=20,
            revenue=0
        )


def test_debt_to_equity_zero_equity():

    with pytest.raises(ValueError):

        service.calculate_debt_to_equity(
            total_debt=20,
            equity=0
        )
def test_analyze():

    result = FinancialAnalysisService.analyze(
        revenue=1000,
        operating_income=200,
        net_income=150,
        total_debt=300,
        equity=600,
        operating_cash_flow=250,
        capital_expenditure=50
    )

    assert result["operating_margin"] == 20.0
    assert result["net_margin"] == 15.0
    assert result["debt_to_equity"] == 0.5
    assert result["free_cash_flow"] == 200

def test_analyze_record():

    from backend.app.ingestion.financial_loader import FinancialRecord

    record = FinancialRecord(
        company_id=1,
        fiscal_year=2025,
        revenue=1000,
        net_income=100,
        assets=2000,
        liabilities=800,
        equity=1200,
        cash=300,
        operating_cash_flow=250
    )

    result = FinancialAnalysisService.analyze_record(
        record
    )

    assert result["net_margin"] == 10.0
    assert result["return_on_assets"] == 5.0
    assert result["return_on_equity"] == (
        100 / 1200 * 100
    )

def test_analyze_record_zero_revenue():

    from backend.app.ingestion.financial_loader import FinancialRecord

    record = FinancialRecord(
        company_id=1,
        fiscal_year=2025,
        revenue=0,
        net_income=100,
        assets=2000,
        liabilities=800,
        equity=1200,
        cash=300,
        operating_cash_flow=250
    )

    with pytest.raises(ValueError):

        FinancialAnalysisService.analyze_record(
            record
        )


def test_analyze_record_zero_assets():

    from backend.app.ingestion.financial_loader import FinancialRecord

    record = FinancialRecord(
        company_id=1,
        fiscal_year=2025,
        revenue=1000,
        net_income=100,
        assets=0,
        liabilities=800,
        equity=1200,
        cash=300,
        operating_cash_flow=250
    )

    with pytest.raises(ValueError):

        FinancialAnalysisService.analyze_record(
            record
        )


def test_analyze_record_zero_equity():

    from backend.app.ingestion.financial_loader import FinancialRecord

    record = FinancialRecord(
        company_id=1,
        fiscal_year=2025,
        revenue=1000,
        net_income=100,
        assets=2000,
        liabilities=800,
        equity=0,
        cash=300,
        operating_cash_flow=250
    )

    with pytest.raises(ValueError):

        FinancialAnalysisService.analyze_record(
            record
        )
def test_get_financial_analysis():

    from backend.app.ingestion.financial_loader import (
        FinancialRecord
    )

    class FakeRepository:

        def get_financial_record(
            self,
            company_id,
            fiscal_year
        ):

            return FinancialRecord(
                company_id=company_id,
                fiscal_year=fiscal_year,
                revenue=1000,
                net_income=100,
                assets=2000,
                liabilities=800,
                equity=1200,
                cash=300,
                operating_cash_flow=250
            )

    repository = FakeRepository()

    result = FinancialAnalysisService.get_financial_analysis(
        repository=repository,
        company_id=1,
        fiscal_year=2025
    )

    assert result is not None

    assert result["company_id"] == 1
    assert result["fiscal_year"] == 2025

    assert result["metrics"]["net_margin"] == 10.0
    assert result["metrics"]["return_on_assets"] == 5.0
    assert result["metrics"]["return_on_equity"] == (
        100 / 1200 * 100
    )

def test_get_financial_analysis_not_found():

    class FakeRepository:

        def get_financial_record(
            self,
            company_id,
            fiscal_year
        ):
            return None

    repository = FakeRepository()

    result = FinancialAnalysisService.get_financial_analysis(
        repository=repository,
        company_id=9999,
        fiscal_year=2099
    )

    assert result is None