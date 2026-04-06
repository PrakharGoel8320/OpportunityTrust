import { Link, NavLink } from 'react-router-dom'

function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar__brand">
        <div className="brandMark">OT</div>
        <div>
          <p className="brandName">Opportunity Trust</p>
          <p className="brandTag">Intelligence Network</p>
        </div>
      </div>

      <nav className="navbar__links">
        <NavLink to="/" className={({ isActive }) => `navLink ${isActive ? 'active' : ''}`}>
          Home
        </NavLink>
        <NavLink to="/how-it-works" className={({ isActive }) => `navLink ${isActive ? 'active' : ''}`}>
          How It Works
        </NavLink>
        <NavLink to="/analyze" className={({ isActive }) => `navLink ${isActive ? 'active' : ''}`}>
          Analyze
        </NavLink>
        <NavLink to="/graph" className={({ isActive }) => `navLink ${isActive ? 'active' : ''}`}>
          Graph Preview
        </NavLink>
      </nav>

      <Link to="/analyze" className="navButton">
        Start Analysis
      </Link>
    </header>
  )
}

export default Navbar