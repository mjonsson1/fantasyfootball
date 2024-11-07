import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="header">
      <div className="logo">Fantasy League Hub</div>
      <nav className="nav">
        <Link to="/">Home</Link>
        <Link to="/roster">Roster</Link>
        <Link to="/analyzer">Injury Impact Analyzer</Link>
        <Link to="/standings">Standings</Link>
        <Link to="/challenges">Weekly Challenges</Link>
        <Link to="/login">Login</Link>
      </nav>
    </header>
  );
};

export default Header;
