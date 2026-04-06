function getNodeLabels(graphData) {
  if (!graphData) {
    return {
      companyLabel: 'Company',
      upiLabel: 'UPI',
      complaintLabel: 'Complaint',
      extraLabel: 'Graph data',
    }
  }

  const companyLabel = graphData.company || graphData.company_name || 'Company'
  const upiLabel = graphData.upi_id || graphData.upi || 'UPI'
  const complaintLabel = graphData.complaint_count !== undefined ? `Complaint ${graphData.complaint_count}` : 'Complaint'
  const extraLabel = graphData.linked_companies?.length ? `${graphData.linked_companies.length} Linked Companies` : 'Connections'

  return {
    companyLabel,
    upiLabel,
    complaintLabel,
    extraLabel,
  }
}

function GraphView({ graphData, title = 'TigerGraph Network' }) {
  const hasRealData = graphData && Object.keys(graphData).length > 0
  const labels = getNodeLabels(graphData)

  if (!hasRealData) {
    return (
      <div className="graphEmptyBox">
        <p className="helperText">No graph data available. Please run analysis first.</p>
      </div>
    )
  }

  return (
    <section className="graphSection panel fadeInUp">
      <div className="sectionHeader">
        <div>
          <p className="sectionKicker">{title}</p>
          <h2>Graph Preview</h2>
        </div>
        <span className="statusPill">Live / Cached</span>
      </div>

      <div className="graphCanvas">
        <div className="graphRow graphRow--top">
          <div className="graphNode graphNode--blue">{labels.companyLabel}</div>
          <div className="graphArrow">→</div>
          <div className="graphNode graphNode--center">{labels.upiLabel}</div>
        </div>

        <div className="graphRow graphRow--bottom">
          <div className="graphNode graphNode--red">{labels.complaintLabel}</div>
          <div className="graphArrow">↔</div>
          <div className="graphNode graphNode--purple">{labels.extraLabel}</div>
        </div>
      </div>

      <div className="jsonBox">
        <p className="explanationTitle">Graph Data</p>
        <pre>{JSON.stringify(graphData, null, 2)}</pre>
      </div>
    </section>
  )
}

export default GraphView