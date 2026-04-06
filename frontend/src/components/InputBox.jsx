function InputBox({ message, setMessage, onAnalyze, loading }) {
  return (
    <section className="panel panel--input">
      <div className="sectionHeader">
        <div>
          <p className="sectionKicker">Message Check</p>
          <h2>Paste the job or internship message</h2>
        </div>
        <span className="statusPill">Live analysis</span>
      </div>

      <textarea
        className="messageBox"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Example: Work from home internship. Pay 499 for registration on abc@upi..."
        rows={9}
      />

      <div className="inputFooter">
        <p className="helperText">We check the text, UPI pattern, and TigerGraph complaints together.</p>
        <button className="primaryButton" onClick={onAnalyze} disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze Message'}
        </button>
      </div>
    </section>
  )
}

export default InputBox