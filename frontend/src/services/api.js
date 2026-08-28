const API_BASE_URL = "http://127.0.0.1:8000";


// ============================================================
// Get Companies
// ============================================================

export async function getCompanies() {

  const response = await fetch(
    `${API_BASE_URL}/companies/`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch companies");
  }

  return response.json();
}


// ============================================================
// Get Company Analytics
// ============================================================

export async function getCompanyAnalytics(companyId) {

  const response = await fetch(
    `${API_BASE_URL}/analytics/${companyId}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch financial analytics");
  }

  return response.json();
}


// ============================================================
// Ask Financial Analyst Agent
// ============================================================

export async function askAnalyst(
  question,
  companyId,
  fiscalYear
) {

  const response = await fetch(
    `${API_BASE_URL}/api/analyst/query`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({
        question: question,
        company_id: Number(companyId),
        fiscal_year: Number(fiscalYear)
      })
    }
  );


  if (!response.ok) {

    const errorText =
      await response.text();

    throw new Error(
      errorText ||
      "Failed to query financial analyst"
    );
  }


  return response.json();
}