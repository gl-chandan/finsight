class Company:
    def __init__(self,name:str,ticker:str,cik:str,industry:str):
        self.name = name
        self.ticker = ticker 
        self.cik = cik
        self.industry = industry

    def __str__(self):
        return f"{self.name}({self.ticker})"