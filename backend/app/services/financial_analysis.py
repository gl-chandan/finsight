from backend.app.repositories.financial_repository import (
    FinancialRepository
)
class FinancialAnalysisService:

    # ==========================================================
    # Existing analysis methods
    # ==========================================================

    @staticmethod
    def calculate_growth(
        current: float,
        previous: float
    ) -> float:

        if previous == 0:
            raise ValueError(
                "Previous value cannot be zero"
            )

        return ((current - previous) / previous) * 100


    @staticmethod
    def calculate_margin(
        profit: float,
        revenue: float
    ) -> float:

        if revenue == 0:
            raise ValueError(
                "Revenue cannot be zero"
            )

        return (profit / revenue) * 100


    @staticmethod
    def calculate_current_ratio(
        current_assets: float,
        current_liabilities: float
    ) -> float:

        if current_liabilities == 0:
            raise ValueError(
                "Current liabilities cannot be zero"
            )

        return current_assets / current_liabilities


    @staticmethod
    def calculate_roa(
        net_income: float,
        total_assets: float
    ) -> float:

        if total_assets == 0:
            raise ValueError(
                "Total assets cannot be zero"
            )

        return (net_income / total_assets) * 100


    @staticmethod
    def calculate_roe(
        net_income: float,
        equity: float
    ) -> float:

        if equity == 0:
            raise ValueError(
                "Equity cannot be zero"
            )

        return (net_income / equity) * 100

    @staticmethod
    def analyze(
        revenue: float,
        operating_income: float,
        net_income: float,
        total_debt: float,
        equity: float,
        operating_cash_flow: float,
        capital_expenditure: float
    ) -> dict:

        return {
            "operating_margin": (
                FinancialAnalysisService.calculate_operating_margin(
                    operating_income,
                    revenue
                )
            ),

            "net_margin": (
                FinancialAnalysisService.calculate_net_margin(
                    net_income,
                    revenue
                )
            ),

            "debt_to_equity": (
                FinancialAnalysisService.calculate_debt_to_equity(
                    total_debt,
                    equity
                )
            ),

            "free_cash_flow": (
                FinancialAnalysisService.calculate_free_cash_flow(
                    operating_cash_flow,
                    capital_expenditure
                )
            )
        }
    @staticmethod
    def analyze_record(record) -> dict:

        return {
            "net_margin": (
                FinancialAnalysisService.calculate_net_margin(
                    record.net_income,
                    record.revenue
                )
            ),

            "return_on_assets": (
                FinancialAnalysisService.calculate_roa(
                    record.net_income,
                    record.assets
                )
            ),

            "return_on_equity": (
                FinancialAnalysisService.calculate_roe(
                    record.net_income,
                    record.equity
                )
            )
        }
    # ==========================================================
    # Day 9 financial metrics
    # ==========================================================

    @staticmethod
    def calculate_operating_margin(
        operating_income: float,
        revenue: float
    ) -> float:

        if revenue == 0:
            raise ValueError(
                "Revenue cannot be zero"
            )

        return (operating_income / revenue) * 100


    @staticmethod
    def calculate_net_margin(
        net_income: float,
        revenue: float
    ) -> float:

        if revenue == 0:
            raise ValueError(
                "Revenue cannot be zero"
            )

        return (net_income / revenue) * 100


    @staticmethod
    def calculate_debt_to_equity(
        total_debt: float,
        equity: float
    ) -> float:

        if equity == 0:
            raise ValueError(
                "Equity cannot be zero"
            )

        return total_debt / equity


    @staticmethod
    def calculate_free_cash_flow(
        operating_cash_flow: float,
        capital_expenditure: float
    ) -> float:

        return (
            operating_cash_flow
            - capital_expenditure
        )
    @staticmethod
    def get_financial_analysis(
        repository: FinancialRepository,
        company_id: int,
        fiscal_year: int
    ):

        record = repository.get_financial_record(
            company_id=company_id,
            fiscal_year=fiscal_year
        )

        if record is None:
            return None

        analysis = FinancialAnalysisService.analyze_record(
            record
        )

        return {
            "company_id": record.company_id,
            "fiscal_year": record.fiscal_year,
            "metrics": analysis
        }