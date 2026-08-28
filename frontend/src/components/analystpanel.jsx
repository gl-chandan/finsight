import { useState } from "react";
import { askAnalyst } from "../services/api";


function AnalystPanel({ companyId, fiscalYear }) {

  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  async function handleAsk() {

    if (!question.trim()) {
      return;
    }

    try {

      setLoading(true);
      setError("");
      setResult(null);

      const data = await askAnalyst(
        question,
        companyId,
        fiscalYear
      );

      setResult(data);

    } catch (error) {

      setError(
        "Unable to get analyst response."
      );

    } finally {

      setLoading(false);

    }

  }


  return (

    <section className="analyst-panel">

      <div className="analyst-header">

        <h2>AI Financial Analyst</h2>

        <p>
          Ask questions about the company's
          financial performance and filings.
        </p>

      </div>


      <div className="analyst-form">

        <textarea
          rows="4"
          value={question}
          placeholder="Ask a financial question..."
          onChange={(event) =>
            setQuestion(event.target.value)
          }
          onKeyDown={(event) => {

            if (
              event.key === "Enter" &&
              !event.shiftKey
            ) {
              event.preventDefault();
              handleAsk();
            }

          }}
        />

        <button
          onClick={handleAsk}
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Ask Analyst"}
        </button>

      </div>


      {error && (

        <p className="error-message">
          {error}
        </p>

      )}


      {result && (

        <div className="analyst-result">

          <div className="analyst-route">

            <span>Route</span>

            <strong>
              {result.route}
            </strong>

          </div>


          <div className="analyst-answer">

            <strong>Answer</strong>

            <p>
              {result.answer}
            </p>

          </div>


          {result.sources &&
            result.sources.length > 0 && (

            <div className="analyst-sources">

              <strong>Sources</strong>

              {result.sources.map(
                (source, index) => (

                  <div
                    key={index}
                    className="source-card"
                  >

                    <strong>
                      {source.document}
                    </strong>

                    <span>
                      Page: {source.page}
                    </span>

                    <p>
                      {source.text}
                    </p>

                  </div>

                )
              )}

            </div>

          )}

        </div>

      )}

    </section>

  );

}


export default AnalystPanel;