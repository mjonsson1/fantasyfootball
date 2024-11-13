import React, { useState, useEffect } from 'react';

const InjuryImpactAnalyzer = () => {
  // Sample state for player injuries
  const [injuries, setInjuries] = useState([]);

  // Example of fetching injury data
  useEffect(() => {
    // Replace this with actual data fetching code (e.g., API call)
    const fetchInjuryData = async () => {
      const data = [
        { name: 'Player A', position: 'WR', team: 'Team X', injury: 'ACL Tear', outWeeks: 10 },
        { name: 'Player B', position: 'RB', team: 'Team Y', injury: 'Concussion', outWeeks: 2 },
        { name: 'Player C', position: 'QB', team: 'Team Z', injury: 'Shoulder Sprain', outWeeks: 3 },
      ];
      setInjuries(data);
    };
    
    fetchInjuryData();
  }, []);

  return (
    <div className="injury-impact-analyzer">
      <h1>Injury Impact Analyzer</h1>
      <p>Check the impact of injuries on players' availability and team performance.</p>

      {/* Injuries Table */}
      <table className="injury-table">
        <thead>
          <tr>
            <th>Player Name</th>
            <th>Position</th>
            <th>Team</th>
            <th>Injury</th>
            <th>Weeks Out</th>
          </tr>
        </thead>
        <tbody>
          {injuries.length > 0 ? (
            injuries.map((player, index) => (
              <tr key={index}>
                <td>{player.name}</td>
                <td>{player.position}</td>
                <td>{player.team}</td>
                <td>{player.injury}</td>
                <td>{player.outWeeks}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="5">No injuries reported.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default InjuryImpactAnalyzer;
