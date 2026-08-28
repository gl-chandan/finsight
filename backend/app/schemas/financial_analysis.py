from pydantic import BaseModel


class FinancialMetrics(BaseModel):

    net_margin: float
    return_on_assets: float
    return_on_equity: float


class FinancialAnalysisResponse(BaseModel):

    company_id: int
    fiscal_year: int
    metrics: FinancialMetrics