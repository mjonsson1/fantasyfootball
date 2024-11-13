import React from 'react';
function RosterManagement() {
  return (
    <main className="roster-management">
      <h1>Your Roster</h1>
      <div className="roster-summary">
        <h2>Total Points: <span id="total-points">123</span></h2>
        <table className="roster-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Position</th>
              <th>Team</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Player A</td>
              <td>WR</td>
              <td>Team X</td>
              <td>Active</td>
              <td>
                <button className="action-btn">Bench</button>
                <button className="action-btn">Drop</button>
              </td>
            </tr>
            <tr>
              <td>Player B</td>
              <td>RB</td>
              <td>Team Y</td>
              <td>Injured</td>
              <td>
                <button className="action-btn">Start</button>
                <button className="action-btn">Drop</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Add Player Section */}
      <div className="add-player-section">
        <h2>Add Player</h2>
        <input type="text" id="search-player" placeholder="Search for a player..." />
        <div className="available-players">
          <div className="player-card">
            <span>Player C (WR) - Team Z</span>
            <button className="action-btn">Add Player</button>
          </div>
          <div className="player-card">
            <span>Player D (QB) - Team W</span>
            <button className="action-btn">Add Player</button>
          </div>
        </div>
      </div>
    </main>
  );
}

export default RosterManagement;