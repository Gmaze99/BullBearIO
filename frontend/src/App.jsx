import React, { useState } from "react";
import "./App.css";

function App() {
  const [ticker, setTicker] = useState("AAPL");
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchAnalysis = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:8000/analysis/${ticker}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setAnalysis(data);
    } catch (error) {
      setError(error.message);
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        BullBear.io 📊
      </div>

      <div className="search-bar">
        <input 
          type="text" 
          value={ticker} 
          onChange={(e) => setTicker(e.target.value)} 
          placeholder="Enter ticker..."
        />
        <button onClick={fetchAnalysis} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="analysis">
        <h2>Analysis for {ticker}</h2>
        <div className="cards">
          <div className="card">
            <h3>📰 Sentiment</h3>
            {analysis ? (
              <>
                <p>Average: {analysis.sentiment.average?.toFixed(2) || "N/A"}</p>
                <p>Articles: {analysis.sentiment.articles_analyzed || 0}</p>
              </>
            ) : (
              <p>No data available</p>
            )}
          </div>

          <div className="card">
            <h3>📈 Price</h3>
            {analysis ? (
              <>
                <p>Current: ${analysis.price?.current?.toFixed(2) || "N/A"}</p>
                <p>Change: {analysis.price?.change_pct?.toFixed(2) || 0}%</p>
              </>
            ) : (
              <p>Run analysis first</p>
            )}
          </div>

          <div className="card">
            <h3>📊 Verdict</h3>
            {analysis ? (
              <p>
                {analysis.verdict.label} (Score: {analysis.verdict.score?.toFixed(2)})
              </p>
            ) : (
              <p>Run analysis first</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;