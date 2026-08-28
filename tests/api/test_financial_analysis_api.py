from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_financial_analysis_api():

    response = client.get(
        "/api/financial-analysis/1/2025"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["company_id"] == 1
    assert data["fiscal_year"] == 2025

    assert "metrics" in data

    assert "net_margin" in data["metrics"]
    assert "return_on_assets" in data["metrics"]
    assert "return_on_equity" in data["metrics"]

def test_financial_analysis_not_found():

    response = client.get(
        "/api/financial-analysis/9999/2099"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Financial record not found"

def test_invalid_company_id():

    response = client.get(
        "/api/financial-analysis/0/2025"
    )

    assert response.status_code == 422


def test_invalid_fiscal_year():

    response = client.get(
        "/api/financial-analysis/1/1990"
    )

    assert response.status_code == 422