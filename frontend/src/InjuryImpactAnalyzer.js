import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './styles.css';

const InjuryImpactAnalyzer = ({ userID }) => {
  const [roster, setRoster] = useState([]);
  const [selectedPlayers, setSelectedPlayers] = useState([]); 
  const [totalScore, setTotalScore] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null); 
  const [errorMessage, setErrorMessage] = useState(null); // State for error message
  const [positionFilter, setPositionFilter] = useState('all'); // State for position filter
  const [sortedRoster, setSortedRoster] = useState([]); // State for sorted roster (for recommendations)
  const [refreshKey, setRefreshKey] = useState(0); // Key to force component refresh
  const id = userID || localStorage.getItem('userID');  // Use userID from state or localStorage

  // Define position limits
  const positionLimits = {
    'K': 1,
    'WR': 2,
    'Offensive Player': 1,
    'P': 1,
    'RB': 2,
    'QB': 1,
    'PR': 1,
    'KR': 1,
    'Defender': 2,
  };

  // Fetch roster data
  const getRoster = async () => {
    const id = userID || localStorage.getItem('userID');
    if (id) {
      try {
        const response = await axios.get(`http://localhost:5000/api/roster/${id}`);
        setRoster(response.data);
        setSortedRoster(response.data);  // Initialize sortedRoster with the original roster
      } catch (error) {
        console.error('Error fetching roster:', error);
      }
    } else {
      console.log('userID is undefined or null');
    }
  };

  // Fetch player stats and calculate injury impact score
  useEffect(() => {
    const fetchPlayerStats = async () => {
      try {
        if (selectedPlayers.length > 0) {
          const response = await axios.post('http://localhost:5000/api/injury-impact', {
            userID: id,
            PlayerIDs: selectedPlayers,
          });
          console.log('API Response:', response.data);
  
          if (response.data.total_score !== undefined) {
            setTotalScore(response.data.total_score);
          } else {
            setTotalScore('Error calculating score');
          }
        } else {
          setTotalScore(0); // Set to 0 if no players are selected
        }
      } catch (error) {
        console.error('Error calculating injury impact:', error);
        setTotalScore('Error calculating score');
      }
    };
  
    fetchPlayerStats();
  }, [selectedPlayers, userID]);

  // Count how many players are selected per position
  const countPlayersByPosition = () => {
    return selectedPlayers.reduce((count, playerID) => {
      const player = roster.find(p => p.PlayerID === playerID);
      if (player) {
        count[player.Position] = (count[player.Position] || 0) + 1;
      }
      return count;
    }, {});
  };

  const togglePlayerSelection = (playerID) => {
    const player = roster.find((p) => p.PlayerID === playerID);
    if (!player) return;

    const positionCount = countPlayersByPosition();
    const position = player.Position;
    const currentSelectionCount = positionCount[position] || 0;
    const maxSelection = positionLimits[position] || 0;

    if (currentSelectionCount < maxSelection || selectedPlayers.includes(playerID)) {
      // Toggle player selection
      setSelectedPlayers((prev) => {
        const updatedSelection = prev.includes(playerID)
          ? prev.filter((id) => id !== playerID)  // Deselect player
          : [...prev, playerID];  // Select player
    
        console.log('Updated selected players:', updatedSelection);  // Check if playerID is correctly toggled
        return updatedSelection;
      });
    } else {
      // Display error message
      setErrorMessage(`You can only select ${maxSelection} player(s) for the position: ${position}`);
      
      // Set a timer to clear the error message after 5 seconds
      setTimeout(() => {
        setErrorMessage(null);
      }, 3000);
    }
  };

  // Recommendations button functionality
  const handleRecommendationsClick = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/recommendations', {
        userID: id, // Send the userID to the backend
      });

      if (response.data.players) {
        const recommendedPlayers = response.data.players; // The sorted player list based on recommendations
        console.log('Recommendations:', recommendedPlayers);

        // Sort the players from the roster based on the recommended player order
        const sortedRosterData = recommendedPlayers.map((recPlayer) => {
          const playerData = roster.find(player => player.PlayerID === recPlayer.PlayerID);
          return playerData; // This maps the PlayerID to its full player data
        });

        console.log('Sorted roster:', sortedRosterData);

        // Update sortedRoster with the newly sorted players
        setSortedRoster(sortedRosterData);
      } else {
        console.error('Players data is missing or in an unexpected format');
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  // Fetch roster when component mounts
  useEffect(() => {
    getRoster();
  }, [userID]);

  // Filter and display recommended players
  const filteredRecommendedPlayers = sortedRoster.filter((player) => !selectedPlayers.includes(player.PlayerID));
  
  // Filter players based on the position filter dropdown
  const filteredInactivePlayers = positionFilter === 'all'
    ? filteredRecommendedPlayers
    : filteredRecommendedPlayers.filter((player) => player.Position === positionFilter);

  return (
    <div className="injury-impact-analyzer">
      <h2>Injury Impact Analyzer</h2>
      <div className="score-section">
        <h3>Total Projected Score</h3>
        <p className="projected-score-text">{totalScore === null ? 'Loading...' : totalScore}</p>
        <div className="score-rectangle" style={{ width: `${totalScore ? Math.min(totalScore * 10, 1000) : 0}px` }}></div>
      </div>


      {successMessage && <p className="success-message">{successMessage}</p>}

      {/* Error message */}
      {errorMessage && (
        <div className="error-message">
          {errorMessage}
        </div>
      )}

      {/* Recommendations Button */}
      <div className="recommendations-section">
        <button className="recommendations-button" onClick={handleRecommendationsClick}>
          Get Recommendations
        </button>
      </div>


      {/* Active Players Section */}
      <div className="player-section active-players">
        <h3>Active Players</h3>
        {roster.length > 0 ? (
          <div className="player-list">
            {roster.filter(player => selectedPlayers.includes(player.PlayerID)).map((player) => (
              <div className="player-card" key={player.PlayerID}>
                <input
                  type="checkbox"
                  id={`player-${player.PlayerID}`}
                  checked={true} // Player is already selected
                  onChange={() => togglePlayerSelection(player.PlayerID)} // Deselect player
                />
                <div className="player-details">
                  <span><strong>{player.PlayerName}</strong></span>
                  <span>{player.Position}</span>
                  <span>{player.TeamAB}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p>No active players selected.</p>
        )}
      </div>

      {/* Position filter dropdown */}
      <div className="position-filter">
        <label htmlFor="position-filter">Filter Inactive Players by Position:</label>
        <select
          id="position-filter"
          value={positionFilter}
          onChange={(e) => setPositionFilter(e.target.value)}
        >
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

      {/* Inactive Players Section (Now Shows Recommended Players) */}
      <div className="player-section inactive-players">
        <h3>Inactive Players</h3>
        {filteredInactivePlayers.length > 0 ? (
          <div className="player-list">
            {filteredInactivePlayers.map((player) => (
              <div className="player-card" key={player.PlayerID}>
                <input
                  type="checkbox"
                  id={`player-${player.PlayerID}`}
                  checked={false} // Player is not selected
                  onChange={() => togglePlayerSelection(player.PlayerID)} // Select player
                />
                <div className="player-details">
                  <span><strong>{player.PlayerName}</strong></span>
                  <span>{player.Position}</span>
                  <span>{player.TeamAB}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p>No inactive players available.</p>
        )}
      </div>
    </div>
  );
};

export default InjuryImpactAnalyzer;