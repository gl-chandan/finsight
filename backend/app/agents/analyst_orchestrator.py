from backend.app.agents.financial_analyst_agent import (
    FinancialAnalystAgent
)


class AnalystOrchestrator:

    def __init__(
        self,
        financial_analyst: FinancialAnalystAgent
    ):
        self.financial_analyst = financial_analyst

    def analyze(
        self,
        question: str,
        company_id: int,
        fiscal_year: int
    ):

        # ------------------------------------------------------
        # Send question to the existing Financial Analyst Agent
        # ------------------------------------------------------

        result = self.financial_analyst.analyze(
            question=question,
            company_id=company_id,
            fiscal_year=fiscal_year
        )

        return result