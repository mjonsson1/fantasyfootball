import React, { useState, useEffect } from 'react';
import axios from 'axios';

function RosterManagement() {
  const [players, setPlayers] = useState([]);  // Manage the list of players
  const [searchTerm, setSearchTerm] = useState('');  // Manage the search term

  // Fetch players when component mounts
  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/players'); 
        setPlayers(response.data);  // Store the fetched players in state
      } catch (error) {
        console.error("Error fetching players:", error);
      }
    };

    fetchPlayers();  // Call the fetch function
  }, []);  // Empty dependency array ensures this runs once when the component mounts

  // Handle search input changes
  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);  // Update the search term state
  };
  

  // Filter players based on the search term
  const filteredPlayers = players.filter(player =>
    player.PlayerName.toLowerCase().includes(searchTerm.toLowerCase())  // Case-insensitive search
  );

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
        <input
          type="text"
          id="search-player"
          placeholder="Search for a player..."
          value={searchTerm}  // Controlled input for search term
          onChange={handleSearchChange}  // Update search term when user types
        />
        <div className="available-players">
          {/* Render filtered list of available players */}
          {filteredPlayers.length > 0 ? (
            filteredPlayers.map((player) => (
              <div key={player.PlayerID} className="player-card">
                <span>{player.PlayerName} ({player.Position}) - Team {player.TeamAB}</span>
                <button className="action-btn">Add Player</button>
              </div>
            ))
          ) : (
            <p>No players found</p>  // Show message if no players match search term
          )}
        </div>
      </div>
    </main>
  );
}

export default RosterManagement;
