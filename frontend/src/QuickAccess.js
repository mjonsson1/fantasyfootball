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
        <h2>Injury Updates</h2>
        <p>Get the latest injury news.</p>
        <a href="analyzer">View Injury Reports</a>
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
