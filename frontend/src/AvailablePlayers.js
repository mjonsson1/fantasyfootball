import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './styles.css'; // Import your CSS file

const AvailablePlayers = () => {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [userID, setUserID] = useState(1); // Assuming you have a way to set the UserID dynamically

  // Fetch available players on component mount
  useEffect(() => {
    axios.get('http://localhost:5000/api/available-players')
      .then(response => {
        setPlayers(response.data);
        setLoading(false); // Set loading to false once data is fetched
      })
      .catch(error => {
        setError('Error fetching available players');
        setLoading(false); // Set loading to false even if there's an error
      });
  }, []);

  // Function to add a player to the roster
  const addPlayerToRoster = (playerID) => {
    axios.post('http://localhost:5000/api/roster', { UserID: userID, PlayerID: playerID })
      .then(response => {
        setSuccessMessage(response.data.message || 'Player added to roster!');
        setTimeout(() => setSuccessMessage(null), 3000); // Clear success message after 3 seconds
      })
      .catch(() => {
        setError('Error adding player to roster');
        setTimeout(() => setError(null), 3000); // Clear error message after 3 seconds
      });
  };

  if (loading) {
    return <p>Loading...</p>; // Show loading message
  }

  return (
    <div className="available-players">
      <h2>Available Players for Draft</h2>
      {error && <p className="error-message">{error}</p>} {/* Display error message if present */}
      {successMessage && <p className="success-message">{successMessage}</p>} {/* Display success message */}
      {players.length > 0 ? (
        <ul className="player-list">
          {players.map(player => (
            <li key={player.PlayerID} className="player-item">
              {player.FirstName} {player.LastName} - {player.Position} ({player.TeamName})
              <button 
                className="add-button" 
                onClick={() => addPlayerToRoster(player.PlayerID)}
              >
                Add to Roster
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p>No players available for draft.</p>
      )}
    </div>
  );
};

export default AvailablePlayers;
