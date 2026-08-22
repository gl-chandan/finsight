from abc import ABC,abstractmethod #abc is abstract base class module (to create template classes)

class FinancialStatement(ABC):               # cannot run FinancialStatement(2026) because it is abstract.
    def __init__(self,fiscal_year:int):
        self.fiscal_year = fiscal_year       # mandatory rule.Any child class (like a Balance Sheet or Income Statement) must implement its own version of calculate_metrics

    @abstractmethod                          # A decorator is a tool that wraps around a function or method to modify its behavior without changing its source code.
    def calculate_metrics(self):
        pass


class IncomeStatement(FinancialStatement):
    def __init__(self,fiscal_year:int,revenue:float,cost_of_revenue:float,operating_income:float,net_income:float):
        super().__init__(fiscal_year)
        self.revenue = revenue
        self.cost_of_revenue = cost_of_revenue
        self.operating_income = operating_income
        self.net_income = net_income

    def calculate_metrics(self):
        gross_profit = (
            self.revenue - self.cost_of_revenue
        )

        gross_margin = (
            gross_profit / self.revenue
        ) * 100

        operating_margin = (
            self.operating_income / self.revenue
        ) * 100

        net_margin = (
            self.net_income / self.revenue
        ) * 100

        return {
            "gross_profit": gross_profit,
            "gross_margin": gross_margin,
            "operating_margin": operating_margin,
            "net_margin": net_margin
        }

class BalanceSheet(FinancialStatement):
    def __init__(self,fiscal_year: int,cash: float,total_assets: float,total_liabilities: float,total_debt: float,equity: float):
        super().__init__(fiscal_year)

        self.cash = cash
        self.total_assets = total_assets
        self.total_liabilities = total_liabilities
        self.total_debt = total_debt
        self.equity = equity

    def calculate_metrics(self):

        if self.equity == 0:
            raise ValueError(
                "Equity cannot be zero"
            )

        debt_to_equity = (
            self.total_debt / self.equity
        )

        return {
            "debt_to_equity": debt_to_equity
        }

class CashFlowStatement(FinancialStatement):
    def __init__(self,fiscal_year: int,operating_cash_flow: float,capital_expenditure: float):
        super().__init__(fiscal_year)

        self.operating_cash_flow = operating_cash_flow
        self.capital_expenditure = capital_expenditure

    def calculate_metrics(self):

        free_cash_flow = (
            self.operating_cash_flow
            - self.capital_expenditure
        )

        return {
            "free_cash_flow": free_cash_flow
        }

