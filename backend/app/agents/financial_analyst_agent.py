from backend.app.services.financial_analysis import (
    FinancialAnalysisService
)

from backend.app.repositories.financial_repository import (
    FinancialRepository
)

from backend.app.rag.rag_service import (
    RAGService
)


class FinancialAnalystAgent:

    def __init__(
        self,
        repository: FinancialRepository,
        rag_service: RAGService
    ):
        self.repository = repository
        self.rag_service = rag_service

    # ==========================================================
    # MAIN ANALYSIS
    # ==========================================================

    def analyze(
        self,
        question: str,
        company_id: int,
        fiscal_year: int
    ):

        question_lower = question.lower()

        # ======================================================
        # 1. DOCUMENT / RAG QUESTIONS
        # ======================================================

        rag_keywords = [
            "why",
            "reason",
            "cause",
            "risk",
            "management",
            "filing",
            "report",
            "mentioned",
            "employee",
            "headcount",
            "future growth"
        ]

        is_rag_question = any(
            keyword in question_lower
            for keyword in rag_keywords
        )

        # ------------------------------------------------------
        # Avoid sending simple financial comparisons to RAG
        # ------------------------------------------------------

        metric_keywords = [
            "revenue",
            "net income",
            "net profit",
            "profit",
            "assets",
            "liabilities",
            "equity",
            "cash",
            "roa",
            "return on assets",
            "roe",
            "return on equity",
            "net margin",
            "debt",
            "growth",
            "increase",
            "decrease",
            "change",
            "compare"
        ]

        is_metric_question = any(
            keyword in question_lower
            for keyword in metric_keywords
        )

        # ------------------------------------------------------
        # Route document questions to RAG
        # ------------------------------------------------------

        if is_rag_question and not (
            "revenue growth" in question_lower
            or "profit growth" in question_lower
            or "net income growth" in question_lower
        ):

            result = self.rag_service.answer(
                question=question
            )

            return {
                "question": question,
                "route": "rag",
                "answer": result["answer"],
                "sources": result.get("sources", []),
                "data": None
            }

        # ======================================================
        # 2. GET FINANCIAL RECORD
        # ======================================================

        record = self.repository.get_financial_record(
            company_id=company_id,
            fiscal_year=fiscal_year
        )

        if record is None:

            return {
                "question": question,
                "route": "metrics",
                "answer": (
                    "Financial data is not available "
                    "for the requested company and year."
                ),
                "data": None
            }

        # ======================================================
        # 3. SIMPLE YEAR-OVER-YEAR QUESTIONS
        # ======================================================

        comparison_keywords = [
            "growth",
            "increase",
            "decrease",
            "change",
            "compare",
            "compared"
        ]

        is_comparison = any(
            keyword in question_lower
            for keyword in comparison_keywords
        )

        if is_comparison:

            previous_record = (
                self.repository.get_financial_record(
                    company_id=company_id,
                    fiscal_year=fiscal_year - 1
                )
            )

            if previous_record is None:

                return {
                    "question": question,
                    "route": "metrics",
                    "answer": (
                        "Comparative analysis requires "
                        f"financial data for both "
                        f"{fiscal_year - 1} and "
                        f"{fiscal_year}."
                    ),
                    "data": None
                }

            # --------------------------------------------------
            # Revenue comparison
            # --------------------------------------------------

            if "revenue" in question_lower:

                result = self._compare_values(
                    previous_record.revenue,
                    record.revenue,
                    "Revenue",
                    fiscal_year - 1,
                    fiscal_year
                )

            # --------------------------------------------------
            # Net income / profit comparison
            # --------------------------------------------------

            elif (
                "net income" in question_lower
                or "net profit" in question_lower
                or "profit" in question_lower
            ):

                result = self._compare_values(
                    previous_record.net_income,
                    record.net_income,
                    "Net income",
                    fiscal_year - 1,
                    fiscal_year
                )

            else:

                result = {
                    "answer": (
                        "I can currently compare revenue "
                        "and net income between years."
                    ),
                    "data": None
                }

            return {
                "question": question,
                "route": "metrics",
                "answer": result["answer"],
                "data": result["data"]
            }

        # ======================================================
        # 4. NON-METRIC QUESTIONS → RAG
        # ======================================================

        if not is_metric_question:

            result = self.rag_service.answer(
                question=question
            )

            return {
                "question": question,
                "route": "rag",
                "answer": result["answer"],
                "sources": result.get("sources", []),
                "data": None
            }

        # ======================================================
        # 5. CALCULATE FINANCIAL METRICS
        # ======================================================

        analysis = FinancialAnalysisService.analyze_record(
            record
        )

        # ======================================================
        # 6. IDENTIFY REQUESTED METRIC
        # ======================================================

        if "revenue" in question_lower:

            answer = (
                f"Revenue: "
                f"{self._format_money(record.revenue)}"
            )

        elif (
            "net income" in question_lower
            or "net profit" in question_lower
            or "profit" in question_lower
        ):

            answer = (
                f"Net income: "
                f"{self._format_money(record.net_income)}"
            )

        elif "assets" in question_lower:

            answer = (
                f"Total assets: "
                f"{self._format_money(record.assets)}"
            )

        elif "liabilities" in question_lower:

            answer = (
                f"Total liabilities: "
                f"{self._format_money(record.liabilities)}"
            )

        elif "equity" in question_lower:

            answer = (
                f"Equity: "
                f"{self._format_money(record.equity)}"
            )

        elif "cash" in question_lower:

            answer = (
                f"Cash: "
                f"{self._format_money(record.cash)}"
            )

        elif (
            "roa" in question_lower
            or "return on assets" in question_lower
        ):

            answer = (
                "Return on Assets (ROA): "
                f"{float(analysis['return_on_assets']):.2f}%"
            )

        elif (
            "roe" in question_lower
            or "return on equity" in question_lower
        ):

            answer = (
                "Return on Equity (ROE): "
                f"{float(analysis['return_on_equity']):.2f}%"
            )

        elif "net margin" in question_lower:

            answer = (
                "Net margin: "
                f"{float(analysis['net_margin']):.2f}%"
            )

        elif "debt" in question_lower:

            debt_to_equity = (
                FinancialAnalysisService
                .calculate_debt_to_equity(
                    record.liabilities,
                    record.equity
                )
            )

            answer = (
                "Debt-to-equity ratio: "
                f"{float(debt_to_equity):.2f}"
            )

        else:

            answer = (
                "The question relates to financial metrics, "
                "but the specific metric could not be identified."
            )

        return {
            "question": question,
            "route": "metrics",
            "answer": answer,
            "data": {
                "financial_record": record,
                "calculated_metrics": analysis
            }
        }

    # ==========================================================
    # MONEY FORMATTER
    # ==========================================================

    @staticmethod
    def _format_money(value):

        if value is None:
            return "N/A"

        value = float(value)

        if abs(value) >= 1_000_000_000:
            return f"${value / 1_000_000_000:.2f}B"

        if abs(value) >= 1_000_000:
            return f"${value / 1_000_000:.2f}M"

        if abs(value) >= 1_000:
            return f"${value / 1_000:.2f}K"

        return f"${value:.2f}"

    # ==========================================================
    # SIMPLE VALUE COMPARISON
    # ==========================================================

    @staticmethod
    def _compare_values(
        previous_value,
        current_value,
        metric_name,
        previous_year,
        current_year
    ):

        if previous_value is None or current_value is None:

            return {
                "answer": (
                    f"{metric_name} data is not available "
                    "for both years."
                ),
                "data": None
            }

        previous_value = float(previous_value)
        current_value = float(current_value)

        difference = current_value - previous_value

        if previous_value != 0:

            percentage_change = (
                difference / previous_value
            ) * 100

        else:

            percentage_change = 0

        if difference > 0:

            direction = "increased"

        elif difference < 0:

            direction = "decreased"

        else:

            direction = "remained unchanged"

        answer = (
            f"{metric_name} in {previous_year}: "
            f"{FinancialAnalystAgent._format_money(previous_value)}\n"
            f"{metric_name} in {current_year}: "
            f"{FinancialAnalystAgent._format_money(current_value)}\n"
            f"{metric_name} {direction} by "
            f"{abs(percentage_change):.2f}%."
        )

        return {
            "answer": answer,
            "data": {
                "previous_year": previous_year,
                "current_year": current_year,
                "previous_value": previous_value,
                "current_value": current_value,
                "percentage_change": percentage_change
            }
        }