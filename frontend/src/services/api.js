const API_BASE_URL = "http://127.0.0.1:8000";


export async function getCompanies() {
  const response = await fetch(
    `${API_BASE_URL}/companies/`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch companies");
  }

  return response.json();
}


export async function getCompanyAnalytics(companyId) {
  const response = await fetch(
    `${API_BASE_URL}/analytics/${companyId}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch financial analytics");
  }

  return response.json();
}