function CompanySelector({ companies, selectedCompany, onCompanyChange }) {
  return (
    <div>
      <label htmlFor="company">
        Select Company
      </label>

      <select
        id="company"
        value={selectedCompany}
        onChange={(event) => onCompanyChange(event.target.value)}
      >
        <option value="">
          Select a company
        </option>

        {companies.map((company) => (
          <option
            key={company.id}
            value={company.id}
          >
            {company.name} ({company.ticker})
          </option>
        ))}
      </select>
    </div>
  );
}

export default CompanySelector;