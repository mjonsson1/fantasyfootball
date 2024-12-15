import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './styles.css'; // Import your CSS file

const AvailablePlayers = ({ userID, setRoster, refreshAvailablePlayers }) => {
  const [players, setPlayers] = useState([]);
  const [searchTerm, setSearchTerm] = useState(''); // Search term state
  const [loading, setLoading] = useState(true); // Loading state
  const [error, setError] = useState(null); // Error state
  const [successMessage, setSuccessMessage] = useState(null); // Success message
  const [positionFilter, setPositionFilter] = useState('all'); // Position filter state

  // Fetch the list of players
  const fetchPlayers = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/players');
      setPlayers(response.data); // Store the fetched players
      setLoading(false); // Set loading to false after data is fetched
    } catch (error) {
      console.error('Error fetching players:', error);
      setError('Failed to load players. Please try again.');
      setLoading(false); // Ensure loading is set to false even on failure
    }
  };

  useEffect(() => {
    fetchPlayers(); // Call the fetch function
  }, [refreshAvailablePlayers]); // Trigger when the refresh function is called

  // Filter players based on the search term and position filter
  const filteredPlayers = players.filter((player) => {
    const matchesSearchTerm = player.PlayerName.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesPosition = positionFilter === 'all' || player.Position === positionFilter;
    return matchesSearchTerm && matchesPosition;
  });

  // Handle search input changes
  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value); // Update the search term state
  };

  // Handle position filter change
  const handlePositionFilterChange = (e) => {
    setPositionFilter(e.target.value); // Update the position filter state
  };

  // Add a player to the roster
  const addPlayerToRoster = async (playerID) => {
    try {
      const response = await axios.post('http://localhost:5000/api/roster', {
        UserID: userID,
        PlayerID: playerID,
      });
      const newPlayer = {
        PlayerID: playerID,
        PlayerName: response.data.PlayerName,
        Position: response.data.Position,
        TeamAB: response.data.TeamAB,
        DraftAvailability: response.data.DraftAvailability,
      };

      setRoster((prevRoster) => [...prevRoster, newPlayer]);

      setSuccessMessage(response.data.message || 'Player added to roster!');
      setTimeout(() => setSuccessMessage(null), 3000); // Clear success message after 3 seconds
    } catch (error) {
      console.error('Error adding player to roster:', error);
      setError('Error adding player to roster.');
      setTimeout(() => setError(null), 3000); // Clear error message after 3 seconds
    }
  };

  if (loading) {
    return <p>Loading...</p>; // Show loading message
  }

  return (
    <div className="add-player-section">
      <h2>Add Player</h2>
      {error && <p className="error-message">{error}</p>} {/* Show error message */}
      {successMessage && <p className="success-message">{successMessage}</p>} {/* Show success message */}

      {/* Search and position filter */}
      <input
        type="text"
        id="search-player"
        placeholder="Search for a player..."
        value={searchTerm} // Controlled input for search term
        onChange={handleSearchChange} // Update search term when user types
      />

      <div className="position-filter">
        <label htmlFor="position-filter">Filter by Position:</label>
        <select id="position-filter" value={positionFilter} onChange={handlePositionFilterChange}>
          <option value="all">All</option>
          <option value="K">K</option>
          <option value="WR">WR</option>
          <option value="Offensive Player">Offensive Player</option>
          <option value="P">P</option>
          <option value="RB">RB</option>
          <option value="QB">QB</option>
          <option value="PR">PR</option>
          <option value="KR">KR</option>
          <option value="Defender">Defender</option>
        </select>
      </div>

      {/* Available players list */}
      <div className="available-players">
        {filteredPlayers.length > 0 ? (
          filteredPlayers.map((player) => (
            <div key={player.PlayerID} className="player-card">
              <span>{player.PlayerName} ({player.Position}) - Team {player.TeamAB}</span>
              <button onClick={() => addPlayerToRoster(player.PlayerID)}>Add to Roster</button>
            </div>
          ))
        ) : (
          <p>No players match your search and filter criteria.</p>
        )}
      </div>
    </div>
  );
};

export default AvailablePlayers;