from app.services.sec_client import SECClient


client = SECClient(
    user_agent="FinSight proninja314@gmail.com"
)

data = client.get_company_facts(
    "0001045810"
)

print(data["entityName"])

print(
    data["facts"]["us-gaap"].keys()
)