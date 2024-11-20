import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AvailablePlayers from './AvailablePlayers';
import './styles.css'; // Import your CSS file

const RosterManagement = ({ userID }) => {
  const [roster, setRoster] = useState([]);

  useEffect(() => {
    const id = userID || localStorage.getItem('userID');
    if (id) {
      axios.get(`http://localhost:5000/api/roster/${id}`)
        .then(response => setRoster(response.data))
        .catch(error => console.error('Error fetching roster:', error));
    } else {
      console.log('userID is undefined or null');
    }
  }, [userID]);

  const handleDraftAvailability = (player) => {
    return player.draft_available ? "Available for Draft" : "Not Available for Draft";
  };

  const handleRemovePlayer = (playerID) => {
    const id = userID || localStorage.getItem('userID');
    if (!id) return;

    axios.delete('http://localhost:5000/api/roster', { data: { UserID: id, PlayerID: playerID } })
      .then(() => {
        // Remove player from local state to update UI
        setRoster(prevRoster => prevRoster.filter(player => player.PlayerID !== playerID));
      })
      .catch(error => {
        console.error('Error removing player:', error);
      });
  };

  return (
    <div className="roster-management">
      <h1>Your Roster</h1>
      {roster.length > 0 ? (
        <div className="roster-summary">
          <table className="roster-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Position</th>
                <th>Team</th>
                <th>Draft Status</th>
                <th>Action</th> {/* Add a column for action */}
              </tr>
            </thead>
            <tbody>
              {roster.map(player => (
                <tr key={player.PlayerID}>
                  <td>{player.FirstName} {player.LastName}</td>
                  <td>{player.Position}</td>
                  <td>{player.TeamName}</td>
                  <td>{handleDraftAvailability(player)}</td>
                  <td>
                    <button
                      className="remove-button"
                      onClick={() => handleRemovePlayer(player.PlayerID)}
                    >
                      Remove from Roster
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>You have no players on your roster yet.</p>
      )}
      <AvailablePlayers />
    </div>
  );
  
};

export default RosterManagement;
