import React from 'react';
import './styles.css';

const Standings = () => {
  return (
    <div className="standings-page">
      <h1>Fantasy League Standings</h1>
      <p>This is a placeholder. The standings will be dynamically populated from the backend once implemented.</p>

      <table className="standings-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Team Name</th>
            <th>Wins</th>
            <th>Losses</th>
            <th>Points</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>1</td>
            <td>Team A</td>
            <td>8</td>
            <td>2</td>
            <td>750</td>
          </tr>
          <tr>
            <td>2</td>
            <td>Team B</td>
            <td>7</td>
            <td>3</td>
            <td>690</td>
          </tr>
          <tr>
            <td>3</td>
            <td>Team C</td>
            <td>6</td>
            <td>4</td>
            <td>670</td>
          </tr>
          <tr>
            <td>4</td>
            <td>Team D</td>
            <td>5</td>
            <td>5</td>
            <td>630</td>
          </tr>
          <tr>
            <td>5</td>
            <td>Team E</td>
            <td>4</td>
            <td>6</td>
            <td>580</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default Standings;
