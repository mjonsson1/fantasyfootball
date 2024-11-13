import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Home';
import RosterManagement from './RosterManagement';
import InjuryImpactAnalyzer from './InjuryImpactAnalyzer';
import Header from './Header';
import './styles.css';
import Standings from './Standings';
import Login from'./Login';
import WeeklyChallenges from './WeeklyChallenges';
function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/roster" element={<RosterManagement />} />
        <Route path="/analyzer" element={<InjuryImpactAnalyzer />} />
        <Route path="/standings" element={<Standings />} />
        <Route path="/login" element={<Login />} />
        <Route path="/challenges" element ={<WeeklyChallenges />} />
      </Routes>
    </Router>
  );
}

export default App;
