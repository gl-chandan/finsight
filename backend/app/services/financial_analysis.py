class FinancialAnalysisService:

    @staticmethod # Isolated: It cannot read or modify any data belonging to the class or its objects.
    def calculate_growth(current:float,previous:float)->float: # The @staticmethod decorator defines a function inside a class that does not depend on the class itself or any of its objects.
        if previous==0:
            raise ValueError("Previous value cannot be zero")
        return ((current - previous)/ previous) * 100
    
    @staticmethod
    def calculate_margin(profit: float,revenue: float) -> float:
        if revenue == 0:
            raise ValueError("Revenue cannot be zero")

        return (profit / revenue) * 100

    @staticmethod
    def calculate_current_ratio(current_assets: float,current_liabilities: float) -> float:
        if current_liabilities == 0:
            raise ValueError("Current liabilities cannot be zero")
        return current_assets / current_liabilities

    # ROA
    @staticmethod
    def calculate_roa(net_income: float,total_assets: float) -> float:
        if total_assets == 0:
            raise ValueError("Total assets cannot be zero")

        return (net_income / total_assets) * 100

    # ROE 

    @staticmethod
    def calculate_roe(net_income: float,equity: float) -> float:
        if equity == 0:
            raise ValueError("Equity cannot be zero")
        return (net_income / equity) * 100
    