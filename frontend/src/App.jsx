import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Analyze from './pages/Analyze'
import HowItWorks from './pages/HowItWorks'
import GraphPreview from './pages/GraphPreview'

function App() {
  return (
    <BrowserRouter>
      <div className="appShell">
        <div className="bgGlow bgGlow--one"></div>
        <div className="bgGlow bgGlow--two"></div>

        <Navbar />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/how-it-works" element={<HowItWorks />} />
          <Route path="/analyze" element={<Analyze />} />
          <Route path="/graph" element={<GraphPreview />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App