import React from 'react';

function WelcomeBanner() {
  return (
    <section className="welcome-banner">
      <h1>Welcome to the Fantasy League Hub</h1>
      <p>Track player stats, manage your roster, and stay updated on injuries.</p>
      <a href="analyzer" className="cta">View Injury Impact Analyzer</a>
    </section>
  );
}

export default WelcomeBanner;
