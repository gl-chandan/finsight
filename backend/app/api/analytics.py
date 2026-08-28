
from fastapi import APIRouter, HTTPException

from backend.app.db.connection import get_connection


router = APIRouter(
    prefix="/analytics",
    tags=["Financial Analytics"],
)


@router.get("/{company_id}")
def get_company_analytics(company_id: int):

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    c.id,
                    c.name,
                    c.ticker,

                    fp.fiscal_year,

                    i.revenue,
                    i.net_income,

                    ROUND(
                        (i.operating_income / NULLIF(i.revenue, 0)) * 100,
                        2
                    ) AS operating_margin,

                    ROUND(
                        (i.net_income / NULLIF(i.revenue, 0)) * 100,
                        2
                    ) AS net_margin,

                    ROUND(
                        b.total_debt / NULLIF(b.equity, 0),
                        2
                    ) AS debt_to_equity,

                    cf.operating_cash_flow,

                    cf.capital_expenditure

                FROM companies c

                JOIN financial_periods fp
                    ON c.id = fp.company_id

                JOIN income_statements i
                    ON fp.id = i.financial_period_id

                JOIN balance_sheets b
                    ON fp.id = b.financial_period_id

                JOIN cash_flow_statements cf
                    ON fp.id = cf.financial_period_id

                WHERE c.id = %s

                ORDER BY fp.fiscal_year DESC

                LIMIT 1;
                """,
                (company_id,),
            )

            row = cursor.fetchone()

            if row is None:

                raise HTTPException(
                    status_code=404,
                    detail="Financial data not found",
                )

            # --------------------------------------------------
            # Safely calculate Free Cash Flow
            # --------------------------------------------------

            operating_cash_flow = row[9]
            capital_expenditure = row[10]

            free_cash_flow = None

            if (
                operating_cash_flow is not None
                and capital_expenditure is not None
            ):

                free_cash_flow = (
                    operating_cash_flow
                    - capital_expenditure
                )

            # --------------------------------------------------
            # Build response
            # --------------------------------------------------

            return {

                "company_id": row[0],

                "company_name": row[1],

                "ticker": row[2],

                "fiscal_year": row[3],

                "revenue": (
                    float(row[4])
                    if row[4] is not None
                    else None
                ),

                "net_income": (
                    float(row[5])
                    if row[5] is not None
                    else None
                ),

                "operating_margin": (
                    float(row[6])
                    if row[6] is not None
                    else None
                ),

                "net_margin": (
                    float(row[7])
                    if row[7] is not None
                    else None
                ),

                "debt_to_equity": (
                    float(row[8])
                    if row[8] is not None
                    else None
                ),

                "free_cash_flow": (
                    float(free_cash_flow)
                    if free_cash_flow is not None
                    else None
                ),
            }

    finally:

        connection.close()

