import React, { useState, useEffect } from 'react';
import axios from 'axios';

const InjuryImpactAnalyzer = () => {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRosterData = async () => {
      try {
        const userID = localStorage.getItem('userID');
        if (!userID) {
          setError('User not logged in');
          setLoading(false);
          return;
        }
        const response = await axios.get(`http://localhost:5000/api/roster/${userID}`);
        setPlayers(response.data);
        setLoading(false);
      } catch (err) {
        setError('Error fetching roster data');
        setLoading(false);
      }
    };
  
    fetchRosterData();
  }, []);
  

  const calculateImpact = (expectedReturnDate) => {
    const currentDate = new Date();
    const returnDate = new Date(expectedReturnDate);
    const diffTime = returnDate - currentDate;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays <= 0) return 'High'; // If the expected return is overdue
    if (diffDays <= 14) return 'Medium'; // Return in less than 2 weeks
    return 'Low'; // Return after 2 weeks
  };

  const handleRemovePlayer = (playerID) => {
    const userID = localStorage.getItem('userID');
    if (!userID) return;

    axios
      .delete('http://localhost:5000/api/roster', {
        data: { UserID: userID, PlayerID: playerID },
      })
      .then(() => {
        setPlayers((prevPlayers) => prevPlayers.filter((player) => player.PlayerID !== playerID));
      })
      .catch((error) => {
        console.error('Error removing player:', error);
      });
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="injury-impact-analyzer">
      <h1>Injury Impact Analyzer</h1>
      <p>Check the impact of injuries on players' availability and team performance.</p>

      <table className="injury-table">
        <thead>
          <tr>
            <th>Player Name</th>
            <th>Position</th>
            <th>Team</th>
            <th>Injury Type</th>
            <th>Start Date</th>
            <th>Expected Return</th>
            <th>Current Status</th>
            <th>Impact</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {players.length > 0 ? (
            players.map((player, index) => (
              <tr key={index}>
                <td>{player.FirstName} {player.LastName}</td>
                <td>{player.Position}</td>
                <td>{player.TeamName}</td>
                <td>{player.InjuryType || 'N/A'}</td>
                <td>{player.StartDate}</td>
                <td>{player.ExpectedReturnDate}</td>
                <td>{player.CurrentStatus}</td>
                <td>{player.ExpectedReturnDate ? calculateImpact(player.ExpectedReturnDate) : 'N/A'}</td>
                <td>
                  <button
                    className="remove-button"
                    onClick={() => handleRemovePlayer(player.PlayerID)}
                  >
                    Remove from Roster
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="9">No players in your active roster.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default InjuryImpactAnalyzer;
