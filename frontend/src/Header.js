import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="header">
      <div className="logo">Fantasy League Hub</div>
      <nav className="nav">
        <Link to="/">Home</Link>
        <Link to="/roster">Roster</Link>

        {/* Hover menu for Features */}
        <div className="dropdown">
          <Link to="#" className="dropdown-link">Features</Link>
          <div className="dropdown-content">
            <Link to="/analyzer">Injury Impact Analyzer</Link>
            <Link to="/challenges">Weekly Challenges</Link>
            <Link to="/standings">Standings</Link>
          </div>
        </div>

        <Link to="/login">Login</Link>
      </nav>
    </header>
  );
};

export default Header;
