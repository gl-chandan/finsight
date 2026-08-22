import pytest
from app.services.financial_analysis import (
    FinancialAnalysisService
)




def test_revenue_growth():

    result = FinancialAnalysisService.calculate_growth(
        current=120,
        previous=100
    )

    assert result == 20


def test_profit_margin():

    result = FinancialAnalysisService.calculate_margin(
        profit=20,
        revenue=100
    )

    assert result == 20


def test_current_ratio():

    result = FinancialAnalysisService.calculate_current_ratio(
        current_assets=200,
        current_liabilities=100
    )

    assert result == 2


def test_roa():

    result = FinancialAnalysisService.calculate_roa(
        net_income=20,
        total_assets=100
    )

    assert result == 20


def test_roe():

    result = FinancialAnalysisService.calculate_roe(
        net_income=30,
        equity=150
    )

    assert result == 20


def test_growth_with_zero_previous_value():

    with pytest.raises(ValueError):

        FinancialAnalysisService.calculate_growth(
            current=100,
            previous=0
        )


def test_margin_with_zero_revenue():

    with pytest.raises(ValueError):

        FinancialAnalysisService.calculate_margin(
            profit=20,
            revenue=0
        )


