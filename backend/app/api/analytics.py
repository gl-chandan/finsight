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

                    cf.operating_cash_flow
                        - cf.capital_expenditure
                        AS free_cash_flow

                FROM companies c

                JOIN financial_periods fp
                    ON c.id = fp.company_id

                JOIN income_statements i
                    ON fp.id = i.financial_period_id

                JOIN balance_sheets b
                    ON fp.id = b.financial_period_id

                JOIN cash_flow_statements cf
                    ON fp.id = cf.financial_period_id

                WHERE c.id = %s;
                """,
                (company_id,),
            )

            row = cursor.fetchone()

            if row is None:
                raise HTTPException(
                    status_code=404,
                    detail="Financial data not found",
                )

            return {
                "company_id": row[0],
                "company_name": row[1],
                "ticker": row[2],
                "revenue": float(row[3]),
                "net_income": float(row[4]),
                "operating_margin": float(row[5]),
                "net_margin": float(row[6]),
                "debt_to_equity": float(row[7]),
                "free_cash_flow": float(row[8]),
            }

    finally:
        connection.close()