from pydantic import BaseModel


class CompanyResponse(BaseModel):
    id: int
    name: str
    ticker: str
    cik: str | None = None
    industry: str | None = None