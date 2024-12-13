import React from 'react';

function QuickAccess() {
  return (
    <section className="quick-access">
      <div className="card">
        <h2>Check Standings</h2>
        <p>Check how each team is faring.</p>
        <a href="Standings">Check Standings</a>
      </div>
      <div className="card">
        <h2>Injury Calculations</h2>
        <p>See how injuries affect your team.</p>
        <a href="analyzer">View Analysis</a>
      </div>
      <div className="card">
        <h2>Roster Management</h2>
        <p>Manage your team roster.</p>
        <a href="roster">Go to Roster</a>
      </div>
    </section>
  );
}

export default QuickAccess;
