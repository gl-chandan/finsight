from backend.app.db.connection import get_connection
from backend.app.ingestion.financial_loader import FinancialRecord


class FinancialRepository:

    # ==========================================================
    # SAVE FINANCIAL RECORD
    # ==========================================================

    def save_financial_record(
        self,
        record: FinancialRecord
    ):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            # -------------------------------------------------
            # 1. Find existing financial period
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT id
                FROM financial_periods
                WHERE company_id = %s
                  AND fiscal_year = %s
                  AND period_type = %s
                """,
                (
                    record.company_id,
                    record.fiscal_year,
                    "FY"
                )
            )

            existing_period = cursor.fetchone()

            if existing_period:

                financial_period_id = existing_period[0]

                print(
                    f"Financial period already exists: "
                    f"{financial_period_id}"
                )

            else:

                # -------------------------------------------------
                # 2. Create financial period
                # -------------------------------------------------

                cursor.execute(
                    """
                    INSERT INTO financial_periods
                    (
                        company_id,
                        fiscal_year,
                        period_type
                    )
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (
                        record.company_id,
                        record.fiscal_year,
                        "FY"
                    )
                )

                financial_period_id = cursor.fetchone()[0]

            # -------------------------------------------------
            # 3. Insert / update income statement
            # -------------------------------------------------

            cursor.execute(
                """
                INSERT INTO income_statements
                (
                    financial_period_id,
                    revenue,
                    net_income
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (financial_period_id)
                DO UPDATE SET
                    revenue = EXCLUDED.revenue,
                    net_income = EXCLUDED.net_income
                """,
                (
                    financial_period_id,
                    record.revenue,
                    record.net_income
                )
            )

            # -------------------------------------------------
            # 4. Insert / update balance sheet
            # -------------------------------------------------

            cursor.execute(
                """
                INSERT INTO balance_sheets
                (
                    financial_period_id,
                    cash,
                    total_assets,
                    total_liabilities,
                    equity
                )
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (financial_period_id)
                DO UPDATE SET
                    cash = EXCLUDED.cash,
                    total_assets = EXCLUDED.total_assets,
                    total_liabilities = EXCLUDED.total_liabilities,
                    equity = EXCLUDED.equity
                """,
                (
                    financial_period_id,
                    record.cash,
                    record.assets,
                    record.liabilities,
                    record.equity
                )
            )

            # -------------------------------------------------
            # 5. Insert / update cash flow statement
            # -------------------------------------------------

            cursor.execute(
                """
                INSERT INTO cash_flow_statements
                (
                    financial_period_id,
                    operating_cash_flow
                )
                VALUES (%s, %s)
                ON CONFLICT (financial_period_id)
                DO UPDATE SET
                    operating_cash_flow =
                        EXCLUDED.operating_cash_flow
                """,
                (
                    financial_period_id,
                    record.operating_cash_flow
                )
            )

            connection.commit()

            return financial_period_id

        except Exception:

            connection.rollback()

            raise

        finally:

            cursor.close()
            connection.close()


    # ==========================================================
    # GET FINANCIAL RECORD
    # ==========================================================

    def get_financial_record(
        self,
        company_id: int,
        fiscal_year: int
    ):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    fp.company_id,
                    fp.fiscal_year,

                    i.revenue,
                    i.net_income,

                    b.total_assets,
                    b.total_liabilities,
                    b.equity,
                    b.cash,

                    c.operating_cash_flow

                FROM financial_periods fp

                LEFT JOIN income_statements i
                    ON i.financial_period_id = fp.id

                LEFT JOIN balance_sheets b
                    ON b.financial_period_id = fp.id

                LEFT JOIN cash_flow_statements c
                    ON c.financial_period_id = fp.id

                WHERE fp.company_id = %s
                  AND fp.fiscal_year = %s
                  AND fp.period_type = 'FY'
                """,
                (
                    company_id,
                    fiscal_year
                )
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return FinancialRecord(
                company_id=row[0],
                fiscal_year=row[1],
                revenue=row[2],
                net_income=row[3],
                assets=row[4],
                liabilities=row[5],
                equity=row[6],
                cash=row[7],
                operating_cash_flow=row[8]
            )

        finally:

            cursor.close()
            connection.close()