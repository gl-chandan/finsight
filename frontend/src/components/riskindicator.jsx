function RiskIndicator({ analytics }) {
  if (!analytics) {
    return null;
  }

  const debtToEquity = Number(
    analytics.debt_to_equity
  );

  let riskLevel = "Low";

  if (debtToEquity > 1) {
    riskLevel = "High";
  } else if (debtToEquity > 0.5) {
    riskLevel = "Moderate";
  }

  return (
    <div className="risk-card">

      <p className="section-label">
        DEBT RISK
      </p>

      <h2>
        {riskLevel}
      </h2>

      <p>
        Debt / Equity: {debtToEquity}
      </p>

    </div>
  );
}

export default RiskIndicator;