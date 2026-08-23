import requests


SEC_BASE_URL = "https://data.sec.gov"


class SECClient:

    def __init__(self, user_agent: str):
        self.user_agent = user_agent

    def _get(self, url: str):

        headers = {
            "User-Agent": self.user_agent
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    def get_company_facts(self, cik: str):

        cik_padded = str(cik).zfill(10)

        url = (
            f"{SEC_BASE_URL}/api/xbrl/companyfacts/"
            f"CIK{cik_padded}.json"
        )

        return self._get(url)

    