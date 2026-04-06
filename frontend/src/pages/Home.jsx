import { Link } from 'react-router-dom'

function Home() {
  return (
    <main className="homePage fadeInUp">
      <section className="hero panel">
        <div className="heroContent">
          <p className="heroKicker">Hackathon Project</p>
          <h1>Opportunity Trust Intelligence Network</h1>
          <p className="heroText">
            A simple scam detector for job and internship messages using text signals, live TigerGraph queries,
            and a beginner-friendly trust score.
          </p>

          <div className="heroActions">
            <Link to="/analyze" className="primaryButton">
              Start Analysis
            </Link>
            <Link to="/how-it-works" className="secondaryButton">
              How It Works
            </Link>
          </div>
        </div>

        <div className="heroCard">
          <div className="pulseCircle"></div>
          <p className="heroCardTitle">What it checks</p>
          <ul className="heroList">
            <li>UPI ID pattern</li>
            <li>Payment, urgency, and offer words</li>
            <li>TigerGraph complaint history</li>
            <li>Trust score and risk level</li>
          </ul>
        </div>
      </section>

      <section className="infoStrip" id="how-it-works">
        <div className="infoCard">
          <h3>Text analysis</h3>
          <p>Looks for suspicious words in the message using simple logic.</p>
        </div>
        <div className="infoCard">
          <h3>Live graph check</h3>
          <p>Calls TigerGraph REST API for complaint data linked to the UPI.</p>
        </div>
        <div className="infoCard">
          <h3>Clear result</h3>
          <p>Shows a trust score, risk color, and explanation in a neat card.</p>
        </div>
      </section>
    </main>
  )
}

export default Home