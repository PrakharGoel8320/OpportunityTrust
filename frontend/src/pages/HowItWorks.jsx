import { Link } from 'react-router-dom'

function HowItWorks() {
  return (
    <main className="pageWrap fadeInUp">
      <section className="pageIntro panel">
        <div>
          <p className="heroKicker">How It Works</p>
          <h1>Simple scam detection flow</h1>
          <p className="heroText small">
            The message goes through text checks, then TigerGraph lookup, and finally the app gives a trust score.
          </p>
        </div>

        <Link to="/analyze" className="primaryButton">
          Start Analysis
        </Link>
      </section>

      <section className="workflowPanel panel">
        <div className="workflowBox">Input Message</div>
        <div className="workflowArrow">→</div>
        <div className="workflowBox workflowBox--accent">AI Processing</div>
        <div className="workflowArrow">→</div>
        <div className="workflowBox workflowBox--blue">TigerGraph Check</div>
        <div className="workflowArrow">→</div>
        <div className="workflowBox workflowBox--green">Trust Score Output</div>
      </section>

      <section className="infoStrip">
        <div className="infoCard">
          <h3>1. Input</h3>
          <p>User pastes a job or internship message.</p>
        </div>
        <div className="infoCard">
          <h3>2. Process</h3>
          <p>Backend extracts UPI, company, and risky words.</p>
        </div>
        <div className="infoCard">
          <h3>3. Graph</h3>
          <p>TigerGraph is checked for complaints and links.</p>
        </div>
      </section>
    </main>
  )
}

export default HowItWorks