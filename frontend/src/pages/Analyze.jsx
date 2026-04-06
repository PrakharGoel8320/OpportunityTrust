import { useState } from 'react'
import InputBox from '../components/InputBox'
import ResultCard from '../components/ResultCard'
import GraphView from '../components/GraphView'

function Analyze() {
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [graphLoading, setGraphLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [graphData, setGraphData] = useState(null)
  const [error, setError] = useState('')
  const [graphError, setGraphError] = useState('')

  async function loadGraph(upiId) {
    if (!upiId) {
      setGraphData(null)
      setGraphError('No UPI found in the analysis result.')
      return
    }

    setGraphLoading(true)
    setGraphError('')

    try {
      const response = await fetch(`http://localhost:5000/graph?upi=${encodeURIComponent(upiId)}`)
      const data = await response.json()

      if (!response.ok) {
        setGraphData(null)
        setGraphError(data.error || 'TigerGraph data could not be loaded.')
        return
      }

      setGraphData(data)
      localStorage.setItem('latestGraphData', JSON.stringify(data))
    } catch (err) {
      setGraphData(null)
      setGraphError('TigerGraph request failed. Please try again.')
    } finally {
      setGraphLoading(false)
    }
  }

  async function handleAnalyze() {
    setError('')
    setGraphError('')
    setResult(null)
    setGraphData(null)

    if (!message.trim()) {
      setError('Please paste a job or internship message first.')
      return
    }

    setLoading(true)

    try {
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
      })

      const data = await response.json()

      if (!response.ok) {
        setError(data.error || 'Something went wrong while analyzing.')
      } else {
        setResult(data)
        localStorage.setItem('latestUpiId', data.input?.upi_id || '')
        loadGraph(data.input?.upi_id)
      }
    } catch (err) {
      setError('Cannot connect to backend. Make sure Flask is running on port 5000.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="analyzePage fadeInUp">
      <section className="pageIntro">
        <div>
          <p className="heroKicker">Analysis Page</p>
          <h1>Check a message before trusting it</h1>
          <p className="heroText small">
            Paste the message below. The app will look for scam signals, call TigerGraph live, and create a trust score.
          </p>
        </div>

        <div className="miniMetrics">
          <div className="metricCard">
            <span>Score</span>
            <strong>100</strong>
          </div>
          <div className="metricCard">
            <span>Risk</span>
            <strong>Dynamic</strong>
          </div>
          <div className="metricCard">
            <span>API</span>
            <strong>Flask + TigerGraph</strong>
          </div>
        </div>
      </section>

      <section className="analysisLayout">
        <InputBox message={message} setMessage={setMessage} onAnalyze={handleAnalyze} loading={loading} />

        <div className="analysisSide">
          <div className={`loadingCard ${loading || graphLoading ? 'show' : ''}`}>
            <div className="spinner"></div>
            <p>{loading ? 'Analyzing message...' : 'Loading TigerGraph data...'}</p>
          </div>

          {error && (
            <div className="errorBox fadeInUp">
              <p>{error}</p>
            </div>
          )}

          {result && <ResultCard result={result} />}

          {graphError && (
            <div className="errorBox fadeInUp">
              <p>{graphError}</p>
            </div>
          )}

          {graphData && <GraphView graphData={graphData} title={`UPI: ${result?.input?.upi_id || 'Unknown'}`} />}
        </div>
      </section>
    </main>
  )
}

export default Analyze