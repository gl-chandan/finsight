function FinancialTable({ analytics }) {
  if (!analytics) {
    return null;
  }

  const rows = [
    ["Revenue", analytics.revenue],
    ["Net Income", analytics.net_income],
    ["Operating Margin", `${analytics.operating_margin}%`],
    ["Net Margin", `${analytics.net_margin}%`],
    ["Debt / Equity", analytics.debt_to_equity],
    ["Free Cash Flow", analytics.free_cash_flow],
  ];

  return (
    <div className="financial-table-container">

      <h2>Financial Overview</h2>

      <table className="financial-table">

        <thead>
          <tr>
            <th>Metric</th>
            <th>Value</th>
          </tr>
        </thead>

        <tbody>

          {rows.map(([metric, value]) => (
            <tr key={metric}>
              <td>{metric}</td>
              <td>{value}</td>
            </tr>
          ))}

        </tbody>

      </table>

    </div>
  );
}

export default FinancialTable;