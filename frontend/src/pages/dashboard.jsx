import { useEffect, useState } from "react";

import CompanySelector from "../components/companyselector";
import CompanyOverview from "../components/companyoverview";
import MetricCard from "../components/metriccard";
import FinancialTable from "../components/financialtable";
import RiskIndicator from "../components/riskindicator";

import {
  getCompanies,
  getCompanyAnalytics,
} from "../services/api";


function Dashboard() {

  const [companies, setCompanies] = useState([]);

  const [selectedCompany, setSelectedCompany] =
    useState("");

  const [analytics, setAnalytics] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  useEffect(() => {

    async function loadCompanies() {

      try {

        const data = await getCompanies();

        setCompanies(data);

      } catch (error) {

        setError(
          "Unable to load companies."
        );

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

      const data =
        await getCompanyAnalytics(companyId);

      setAnalytics(data);

    } catch (error) {

      setError(
        "Unable to load financial analytics."
      );

    } finally {

      setLoading(false);

    }

  }


  return (

    <div className="dashboard">

      {/* Header */}

      <header className="dashboard-header">

        <div>

          <h1>FinSight</h1>

          <p>
            AI-Powered Financial
            Due Diligence Platform
          </p>

        </div>

      </header>


      {/* Company Selector */}

      <section className="dashboard-section">

        <CompanySelector
          companies={companies}
          selectedCompany={selectedCompany}
          onCompanyChange={handleCompanyChange}
        />

      </section>


      {/* Loading */}

      {loading && (
        <p className="status-message">
          Loading financial data...
        </p>
      )}


      {/* Error */}

      {error && (
        <p className="error-message">
          {error}
        </p>
      )}


      {/* Dashboard */}

      {analytics && (

        <>

          <CompanyOverview
            analytics={analytics}
          />


          {/* Metrics */}

          <section className="metrics-grid">

            <MetricCard
              title="Revenue"
              value={analytics.revenue}
            />

            <MetricCard
              title="Net Income"
              value={analytics.net_income}
            />

            <MetricCard
              title="Operating Margin"
              value={`${analytics.operating_margin}%`}
            />

            <MetricCard
              title="Net Margin"
              value={`${analytics.net_margin}%`}
            />

            <MetricCard
              title="Debt / Equity"
              value={analytics.debt_to_equity}
            />

            <MetricCard
              title="Free Cash Flow"
              value={analytics.free_cash_flow}
            />

          </section>


          {/* Lower section */}

          <section className="dashboard-grid">

            <FinancialTable
              analytics={analytics}
            />

            <RiskIndicator
              analytics={analytics}
            />

          </section>

        </>

      )}

    </div>

  );
}


export default Dashboard;