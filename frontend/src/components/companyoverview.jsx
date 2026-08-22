function CompanyOverview({ analytics }) {
  if (!analytics) {
    return null;
  }

  return (
    <div className="company-overview">

      <div>
        <p className="section-label">
          COMPANY
        </p>

        <h2>
          {analytics.company_name}
        </h2>
      </div>

      <div>
        <p className="section-label">
          TICKER
        </p>

        <h3>
          {analytics.ticker}
        </h3>
      </div>

    </div>
  );
}

export default CompanyOverview;