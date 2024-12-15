import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AvailablePlayers from './AvailablePlayers';
import './styles.css'; // Import your CSS file

const RosterManagement = ({userID}) => {
  const [roster, setRoster] = useState([]);
  const [players, setPlayers] = useState([]);  // Manage the list of players
  const [searchTerm, setSearchTerm] = useState('');  // Manage the search term
  const [successMessage, setSuccessMessage] = useState(null);  // Success message state
  const [rosterSizeInfo, setRosterSizeInfo] = useState({ current: 0, max: 50 });


const getRosterSize = async () => {
  const id = userID || localStorage.getItem('userID');
  if (id) {
    try {
      const response = await axios.get(`http://localhost:5000/api/roster_size?UserID=${id}`);
      console.log("Roster size response:", response.data);

      const currentRosterSize = Number(response.data.current_roster_size) || 0;
      const maxRosterSize = Number(response.data.max_roster_size) || 50;

      setRosterSizeInfo({ current: currentRosterSize, max: maxRosterSize });
    } catch (error) {
      console.error('Error fetching roster size:', error.response ? error.response.data : error.message);
    }
  }
};

useEffect(() => {
  getRosterSize();  // Fetch roster size data when roster changes
}, [roster, userID]);  // Runs when roster or userID changes


  const getRoster = async () => {
    const id = userID || localStorage.getItem('userID');  // Use userID from state or localStorage
    // console.log("userID: ", id)

    if (id) {
      try {
        const response = await axios.get(`http://localhost:5000/api/roster/${id}`);
        setRoster(response.data);  // Store the fetched roster
      } catch (error) {
        console.error('Error fetching roster:', error);
      }
    } else {
      console.log('userID is undefined or null');
    }
  };

  const getAvailablePlayers = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/players');
      setPlayers(response.data);  // Store the fetched available players
    } catch (error) {
      console.error('Error fetching available players:', error);
    }
  };

  // Refresh roster data
  const refreshRoster = () => {
    getRoster();  // Re-fetch the roster data when refresh button is clicked
    getAvailablePlayers();
  };

  useEffect(() => {
    getRoster();  // Initial fetch of roster when component mounts
    getAvailablePlayers();
  }, [userID]);  // Runs when userID changes
  const removePlayerFromRoster = async (playerID) => {
    const id = userID || localStorage.getItem('userID');
    try {
      const response = await axios.delete('http://localhost:5000/api/roster', {
        data: {
          UserID: id,
          PlayerID: playerID,
        },
      });
      // Filter out the player from the roster list after successful removal
      setRoster(roster.filter(player => player.PlayerID !== playerID));
      // alert(response.data.message || 'Player removed from roster');
      setSuccessMessage(response.data.message || 'Player removed from roster');
      setTimeout(() => setSuccessMessage(null), 3000); // Clear success message after 3 seconds
    } catch (error) {
      console.error('Error removing player from roster:', error);
      alert('Error removing player from roster');
    }
  };
  const handleDraftAvailability = (player) => {
    return player.draft_availability ? "Available for Draft" : "Drafted";
  };
  // Handle search input changes
  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);  // Update the search term state
  };
  

  // Filter players based on the search term
  const filteredPlayers = players.filter(player =>
    player.PlayerName.toLowerCase().includes(searchTerm.toLowerCase())  // Case-insensitive search
  );

  return (
    <div className="roster-management">
    <div className="roster-size-counter">
      <p>Remaining Roster Space: {isNaN(rosterSizeInfo.max) || isNaN(rosterSizeInfo.current) ? "Invalid Data" : rosterSizeInfo.max - rosterSizeInfo.current}</p>
    </div>



      <h1>Your Roster</h1>
      {successMessage && <p className="success-message">{successMessage}</p>} {/* Show success message */}
      {roster.length > 0 ? (
        <div className="roster-summary">
          <table className="roster-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Position</th>
                <th>Team</th>
                <th>Draft Status</th>
                <th>Modify</th>
              </tr>
            </thead>
            <tbody>
              {roster.map((player) => (
                <tr key={player.PlayerID}>
                  <td>{player.PlayerName}</td>
                  <td>{player.Position}</td>
                  <td>{player.TeamAB}</td>
                  <td>{handleDraftAvailability(player)}</td>
                  <td>
                    <button
                      className="remove-btn"
                      onClick={() => removePlayerFromRoster(player.PlayerID)}
                    >
                      Remove
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
      
      <AvailablePlayers 
        userID={userID || localStorage.getItem('userID')} 
        setRoster={setRoster}  // Pass setRoster function to AvailablePlayers
        refreshAvailablePlayers={getAvailablePlayers}  // Pass refresh function to AvailablePlayers
      />
    </div>
  );
};
export default RosterManagement;