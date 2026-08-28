from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    Depends
)

from backend.app.repositories.financial_repository import (
    FinancialRepository
)

from backend.app.services.financial_analysis import (
    FinancialAnalysisService
)

from backend.app.schemas.financial_analysis import (
    FinancialAnalysisResponse
)

from backend.app.core.dependencies import (
    get_financial_repository
)

router = APIRouter(
    prefix="/api/financial-analysis",
    tags=["Financial Analysis"]
)


@router.get(
    "/{company_id}/{fiscal_year}",
    response_model=FinancialAnalysisResponse
)
def get_financial_analysis(
    company_id: int = Path(gt=0),
    fiscal_year: int = Path(
        ge=2000,
        le=2100
    ),
    repository: FinancialRepository = Depends(
        get_financial_repository
    )
):

    result = FinancialAnalysisService.get_financial_analysis(
    repository=repository,
    company_id=company_id,
    fiscal_year=fiscal_year
)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Financial record not found"
        )

    return result