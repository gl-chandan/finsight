from dataclasses import dataclass

from backend.app.services.sec_client import SECClient

# ============================================================
# SEC XBRL TAGS
# ============================================================

REVENUE_TAGS = [
    "Revenues",
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "SalesRevenueNet",
]

NET_INCOME_TAGS = [
    "NetIncomeLoss",
]

ASSETS_TAGS = [
    "Assets",
]

LIABILITIES_TAGS = [
    "Liabilities",
]

EQUITY_TAGS = [
    "StockholdersEquity",
    "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
]

CASH_TAGS = [
    "CashAndCashEquivalentsAtCarryingValue",
]

OPERATING_CASH_FLOW_TAGS = [
    "NetCashProvidedByUsedInOperatingActivities",
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def extract_fact(
    facts: dict,
    possible_tags: list[str]
):
    """
    Return the first available XBRL fact
    from the supplied list of possible tags.
    """

    for tag in possible_tags:

        if tag not in facts:
            continue

        units = facts[tag].get("units", {})

        for unit_name, values in units.items():

            if values:
                return values

    return None


def normalize_fact_values(values: list[dict]):
    """
    Normalize SEC XBRL fact records into a simpler structure.
    """

    normalized = []

    for item in values:

        normalized.append({
            "value": item.get("val"),
            "unit": item.get("form"),
            "start": item.get("start"),
            "end": item.get("end"),
            "fiscal_year": item.get("fy"),
            "fiscal_period": item.get("fp"),
            "filed": item.get("filed"),
            "form": item.get("form"),
        })

    return normalized


def get_annual_value(
    values: list[dict],
    fiscal_year: int
):
    """
    Return the annual financial value for a given fiscal year.
    """

    for item in values:

        if item.get("fiscal_year") != fiscal_year:
            continue

        if item.get("fiscal_period") != "FY":
            continue

        return item

    return None


def extract_annual_fact(
    facts: dict,
    possible_tags: list[str],
    fiscal_year: int
):
    """
    Extract a financial fact for a specific annual fiscal year.
    """

    values = extract_fact(
        facts,
        possible_tags
    )

    if values is None:
        return None

    normalized_values = normalize_fact_values(
        values
    )

    return get_annual_value(
        normalized_values,
        fiscal_year
    )


# ============================================================
# FINANCIAL DATA LOADER
# ============================================================

class FinancialDataLoader:

    def __init__(
        self,
        sec_client: SECClient
    ):
        self.sec_client = sec_client

    def load_company_facts(
        self,
        cik: str,
        fiscal_year: int
    ):
        """
        Load annual financial facts for a company
        for a specific fiscal year.
        """

        data = self.sec_client.get_company_facts(
            cik
        )

        us_gaap = data.get(
            "facts",
            {}
        ).get(
            "us-gaap",
            {}
        )

        return {
            "revenue": extract_annual_fact(
                us_gaap,
                REVENUE_TAGS,
                fiscal_year
            ),

            "net_income": extract_annual_fact(
                us_gaap,
                NET_INCOME_TAGS,
                fiscal_year
            ),

            "assets": extract_annual_fact(
                us_gaap,
                ASSETS_TAGS,
                fiscal_year
            ),

            "liabilities": extract_annual_fact(
                us_gaap,
                LIABILITIES_TAGS,
                fiscal_year
            ),

            "equity": extract_annual_fact(
                us_gaap,
                EQUITY_TAGS,
                fiscal_year
            ),

            "cash": extract_annual_fact(
                us_gaap,
                CASH_TAGS,
                fiscal_year
            ),

            "operating_cash_flow": extract_annual_fact(
                us_gaap,
                OPERATING_CASH_FLOW_TAGS,
                fiscal_year
            ),
        }
    def create_financial_record(
    self,
    company_id: int,
    fiscal_year: int,
    cik: str
):
        """
        Create a FinancialRecord from SEC financial data.
        """

        data = self.load_company_facts(
            cik,
            fiscal_year
        )

        def get_value(
            fact: dict | None
        ):
            if fact is None:
                return None

            return fact.get("value")

        return FinancialRecord(
            company_id=company_id,
            fiscal_year=fiscal_year,
            revenue=get_value(data["revenue"]),
            net_income=get_value(data["net_income"]),
            assets=get_value(data["assets"]),
            liabilities=get_value(data["liabilities"]),
            equity=get_value(data["equity"]),
            cash=get_value(data["cash"]),
            operating_cash_flow=get_value(
                data["operating_cash_flow"]
            )
        )


# ============================================================
# FINANCIAL RECORD
# ============================================================


@dataclass
class FinancialRecord:

    company_id: int
    fiscal_year: int | None

    revenue: float | None = None
    net_income: float | None = None
    assets: float | None = None
    liabilities: float | None = None
    equity: float | None = None
    cash: float | None = None
    operating_cash_flow: float | None = None

def validate_financial_record(
    record: FinancialRecord
):
    """
    Validate a FinancialRecord before storing it.
    """

    if record.company_id <= 0:
        raise ValueError(
            "company_id must be greater than 0"
        )

    if record.fiscal_year is None:
        raise ValueError(
            "fiscal_year cannot be None"
        )

    if record.fiscal_year < 1900:
        raise ValueError(
            "Invalid fiscal year"
        )

    if record.revenue is not None and record.revenue < 0:
        raise ValueError(
            "Revenue cannot be negative"
        )

    if record.assets is not None and record.assets < 0:
        raise ValueError(
            "Assets cannot be negative"
        )

    if record.cash is not None and record.cash < 0:
        raise ValueError(
            "Cash cannot be negative"
        )

    return True