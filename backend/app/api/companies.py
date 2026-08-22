from fastapi import APIRouter, HTTPException

from backend.app.db.connection import get_connection


router = APIRouter(
    prefix="/companies",
    tags=["Companies"],
)


@router.get("/")
def get_companies():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    ticker,
                    cik,
                    industry
                FROM companies
                ORDER BY name;
                """
            )

            rows = cursor.fetchall()

            return [
                {
                    "id": row[0],
                    "name": row[1],
                    "ticker": row[2],
                    "cik": row[3],
                    "industry": row[4],
                }
                for row in rows
            ]

    finally:
        connection.close()


@router.get("/{company_id}")
def get_company(company_id: int):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    ticker,
                    cik,
                    industry
                FROM companies
                WHERE id = %s;
                """,
                (company_id,),
            )

            row = cursor.fetchone()

            if row is None:
                raise HTTPException(
                    status_code=404,
                    detail="Company not found",
                )

            return {
                "id": row[0],
                "name": row[1],
                "ticker": row[2],
                "cik": row[3],
                "industry": row[4],
            }

    finally:
        connection.close()