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

from app.services.sec_client import SECClient


class FinancialDataLoader:

    def __init__(self, sec_client: SECClient):
        self.sec_client = sec_client

    def load_company_facts(self, cik: str):

        data = self.sec_client.get_company_facts(cik)

        us_gaap = data.get(
            "facts",
            {}
        ).get(
            "us-gaap",
            {}
        )

        return {
            "revenue": extract_fact(
                us_gaap,
                REVENUE_TAGS
            ),

            "net_income": extract_fact(
                us_gaap,
                NET_INCOME_TAGS
            ),

            "assets": extract_fact(
                us_gaap,
                ASSETS_TAGS
            ),

            "liabilities": extract_fact(
                us_gaap,
                LIABILITIES_TAGS
            ),

            "equity": extract_fact(
                us_gaap,
                EQUITY_TAGS
            ),

            "cash": extract_fact(
                us_gaap,
                CASH_TAGS
            ),

            "operating_cash_flow": extract_fact(
                us_gaap,
                OPERATING_CASH_FLOW_TAGS
            ),
        }
from dataclasses import dataclass


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