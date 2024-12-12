import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from './Home';
import RosterManagement from './RosterManagement';
import InjuryImpactAnalyzer from './InjuryImpactAnalyzer';
import Header from './Header';
import './styles.css';
import Standings from './Standings';
import Login from './Login';
import WeeklyChallenges from './WeeklyChallenges';

function App() {
  const [isUserLoggedIn, setIsUserLoggedIn] = useState(false);
  const [userID, setUserID] = useState(localStorage.getItem('userID'));

  // Check if there's a token in localStorage to maintain session
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      setIsUserLoggedIn(true);
    } else {
      setIsUserLoggedIn(false); // Reset to false if there's no token
    }
  }, []);

  // Handle login (called by Login.js)
  const handleLogin = (id) => {
    setIsUserLoggedIn(true);
    setUserID(id); // Update userID when logged in
    localStorage.setItem('userID', id); // Store userID in localStorage
  };

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('userID'); // Remove userID on logout
    setIsUserLoggedIn(false);
    setUserID(null); // Reset userID
  };

  return (
    <Router>
      <Header onLogout={handleLogout} />
      <Routes>
        <Route path="/" element={<Home />} />
        {/* Protected Routes */}
        <Route
          path="/roster"
          element={isUserLoggedIn ? <RosterManagement userID={userID} /> : <Navigate to="/login" />}
        />
        <Route
          path="/analyzer"
          element={isUserLoggedIn ? <InjuryImpactAnalyzer userID={userID} /> : <Navigate to="/login" />}
        />
        <Route
          path="/standings"
          element={isUserLoggedIn ? <Standings userID={userID} /> : <Navigate to="/login" />}
        />
        <Route
          path="/challenges"
          element={isUserLoggedIn ? <WeeklyChallenges userID={userID} /> : <Navigate to="/login" />}
        />
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
      </Routes>
    </Router>
  );
}

export default App;
