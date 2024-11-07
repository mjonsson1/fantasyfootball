import React from 'react';

function Featured() {
  return (
    <section className="featured">
      <h2>Recent Updates</h2>
      <div className="updates">
        <div className="update">
          <h3>Injury News</h3>
          <p>Player A is out for the season due to injury.</p>
        </div>
        <div className="update">
          <h3>Top Performers</h3>
          <p>Player B scored 25 points last game!</p>
        </div>
      </div>
    </section>
  );
}

export default Featured;
