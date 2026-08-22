import { useEffect, useState } from "react";

import CompanySelector from "../components/companyselector";
import {
  getCompanies,
  getCompanyAnalytics,
} from "../services/api";


function Dashboard() {

  const [companies, setCompanies] = useState([]);

  const [selectedCompany, setSelectedCompany] = useState("");

  const [analytics, setAnalytics] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  useEffect(() => {

    async function loadCompanies() {

      try {

        const data = await getCompanies();

        setCompanies(data);

      } catch (error) {

        setError("Unable to load companies.");

      }

    }

    loadCompanies();

  }, []);


  async function handleCompanyChange(companyId) {

    setSelectedCompany(companyId);

    if (!companyId) {
      setAnalytics(null);
      return;
    }

    try {

      setLoading(true);
      setError("");

      const data = await getCompanyAnalytics(companyId);

      setAnalytics(data);

    } catch (error) {

      setError("Unable to load financial analytics.");

    } finally {

      setLoading(false);

    }
  }


  return (

    <div>

      <h1>FinSight</h1>

      <p>
        AI-Powered Financial Due Diligence Platform
      </p>


      <CompanySelector
        companies={companies}
        selectedCompany={selectedCompany}
        onCompanyChange={handleCompanyChange}
      />


      {loading && (
        <p>Loading financial data...</p>
      )}


      {error && (
        <p>{error}</p>
      )}


      {analytics && (

        <div>

          <h2>
            {analytics.company_name}
          </h2>

          <p>
            Ticker: {analytics.ticker}
          </p>

          <p>
            Revenue: {analytics.revenue}
          </p>

          <p>
            Net Income: {analytics.net_income}
          </p>

          <p>
            Operating Margin:
            {analytics.operating_margin}%
          </p>

          <p>
            Net Margin:
            {analytics.net_margin}%
          </p>

          <p>
            Debt / Equity:
            {analytics.debt_to_equity}
          </p>

          <p>
            Free Cash Flow:
            {analytics.free_cash_flow}
          </p>

        </div>

      )}

    </div>

  );
}


export default Dashboard;