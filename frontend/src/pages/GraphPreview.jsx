import { useEffect, useState } from 'react'
import GraphView from '../components/GraphView'
import { Link } from 'react-router-dom'

function GraphPreview() {
  const [upiId, setUpiId] = useState('')
  const [graphData, setGraphData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const savedUpi = localStorage.getItem('latestUpiId') || ''
    const savedGraph = localStorage.getItem('latestGraphData')

    setUpiId(savedUpi)

    if (savedGraph) {
      try {
        setGraphData(JSON.parse(savedGraph))
      } catch (err) {
        localStorage.removeItem('latestGraphData')
      }
    }

    if (savedUpi) {
      loadGraph(savedUpi)
    }
  }, [])

  async function loadGraph(customUpiId) {
    setError('')

    const finalUpiId = customUpiId || upiId

    if (!finalUpiId) {
      setGraphData(null)
      setError('No graph data available. Please run analysis first.')
      return
    }

    setLoading(true)

    try {
      const response = await fetch(`http://localhost:5000/graph?upi=${encodeURIComponent(finalUpiId)}`)
      const data = await response.json()

      if (!response.ok) {
        setGraphData(null)
        setError(data.error || 'Graph data could not be loaded.')
        return
      }

      if (!data || Object.keys(data).length === 0) {
        setGraphData(null)
        setError('No graph data available for this UPI.')
        return
      }

      setGraphData(data)
      localStorage.setItem('latestGraphData', JSON.stringify(data))
      setUpiId(finalUpiId)
    } catch (err) {
      setGraphData(null)
      setError('TigerGraph failed. Please check backend and graph query settings.')
    } finally {
      setLoading(false)
    }
  }

  const hasNoData = !upiId && !graphData && !loading

  return (
    <main className="pageWrap fadeInUp">
      <section className="pageIntro panel">
        <div>
          <p className="heroKicker">Graph Preview</p>
          <h1>Live TigerGraph view</h1>
          <p className="heroText small">
            This page shows the graph connected to the latest analyzed UPI. You can load it again with one button.
          </p>
        </div>

        <div className="pageActions">
          <Link to="/analyze" className="secondaryButton">Analyze Message</Link>
          <button className="primaryButton" onClick={loadGraph} disabled={loading}>
            {loading ? 'Loading...' : 'Load Graph'}
          </button>
        </div>
      </section>

      {hasNoData && !error && (
        <div className="emptyState panel">
          <p>No graph data available. Please run analysis first.</p>
        </div>
      )}

      {error && <div className="errorBox fadeInUp"><p>{error}</p></div>}

      {graphData && <GraphView graphData={graphData} title={`UPI: ${upiId || 'Unknown'}`} />}
    </main>
  )
}

export default GraphPreview