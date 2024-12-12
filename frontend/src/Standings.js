import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Standings = () => {
  const [standings, setStandings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStandings = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/standings'); // Adjust endpoint if needed
        setStandings(response.data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchStandings();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  // Group the standings by week
  const groupedStandings = standings.reduce((acc, curr) => {
    const week = curr.Week;
    if (!acc[week]) {
      acc[week] = [];
    }
    acc[week].push(curr);
    return acc;
  }, {});

  return (
    <div className="Standings">
      <header>
        <h1>Fantasy Football Weekly Standings</h1>
      </header>
      <table>
        <thead>
          <tr>
            <th>Week</th>
            <th>User</th>
            <th>Record</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {Object.keys(groupedStandings).map((week) => (
            groupedStandings[week].map((user, index) => (
              <tr key={index}>
                <td>{week}</td>
                <td>{user.FirstName} {user.LastName}</td>
                <td>{user.Record}</td>
                <td>
                  {user.UserID === 1 ? `User 1: ${user.User1_Score}` : `User 2: ${user.User2_Score}`}
                </td>
              </tr>
            ))
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Standings;
