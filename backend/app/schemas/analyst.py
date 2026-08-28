from pydantic import BaseModel


class AnalystQueryRequest(BaseModel):
    question: str
    company_id: int = 1
    fiscal_year: int = 2025


class AnalystQueryResponse(BaseModel):
    question: str
    route: str
    answer: str | None
    data: dict | None = None