import { useEffect, useState } from 'react'

function getRiskClass(riskLevel) {
  if (riskLevel === 'Low') return 'riskLow'
  if (riskLevel === 'Medium') return 'riskMedium'
  return 'riskHigh'
}

function getRiskIcon(riskLevel) {
  if (riskLevel === 'Low') return 'Safe'
  if (riskLevel === 'Medium') return 'Watch'
  return 'Risk'
}

function splitExplanation(explanation) {
  if (!explanation) return []
  return explanation
    .split('.')
    .map((item) => item.trim())
    .filter(Boolean)
}

function ResultCard({ result }) {
  const [barWidth, setBarWidth] = useState('0%')
  const explanationItems = splitExplanation(result?.explanation)
  const trustScore = result?.trust_score ?? 0
  const graphData = result?.graph_data || {}

  useEffect(() => {
    const timer = setTimeout(() => {
      setBarWidth(`${trustScore}%`)
    }, 100)

    return () => clearTimeout(timer)
  }, [trustScore])

  return (
    <section className="panel panel--result fadeInUp">
      <div className="sectionHeader">
        <div>
          <p className="sectionKicker">Analysis Result</p>
          <h2>Trust report</h2>
        </div>
        <div className={`riskBadge ${getRiskClass(result?.risk_level)}`}>
          <span className="riskDot"></span>
          {getRiskIcon(result?.risk_level)} {result?.risk_level || 'Unknown'}
        </div>
      </div>

      <div className="scoreHeader">
        <div>
          <p className="scoreLabel">Trust Score</p>
          <h3>{trustScore}/100</h3>
        </div>
        <p className="scoreNote">
          Higher score means the message looks safer. Lower score means more scam signals.
        </p>
      </div>

      <div className="scoreBar">
        <div className="scoreFill" style={{ width: barWidth }}></div>
      </div>

      <div className="resultGrid">
        <div className="resultStat">
          <span>Company</span>
          <strong>{result?.input?.company_name || 'Unknown'}</strong>
        </div>
        <div className="resultStat">
          <span>UPI ID</span>
          <strong>{result?.input?.upi_id || 'Not found'}</strong>
        </div>
        <div className="resultStat">
          <span>TigerGraph Complaints</span>
          <strong>{graphData.complaint_count ?? 0}</strong>
        </div>
        <div className="resultStat">
          <span>Linked Companies</span>
          <strong>{graphData.linked_companies?.length || 0}</strong>
        </div>
      </div>

      <div className="explanationBox">
        <p className="explanationTitle">Explanation</p>
        <p className="explanationText">{result?.explanation || 'No explanation available.'}</p>
      </div>

      <details className="detailsBox">
        <summary>Why this is risky?</summary>
        <div className="detailsContent">
          {explanationItems.length > 0 ? (
            <ul>
              {explanationItems.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          ) : (
            <p>No extra risk details found.</p>
          )}
        </div>
      </details>

      {result?.tigergraph_warning && (
        <div className="warningBox">
          <p className="explanationTitle">TigerGraph Note</p>
          <p>{result.tigergraph_warning}</p>
        </div>
      )}
    </section>
  )
}

export default ResultCard