import React, { useState } from 'react';
import './styles.css';

const WeeklyChallenges = () => {
  const [challenges, setChallenges] = useState([
    { id: 1, title: "Score 50+ Points", description: "Score 50 or more points this week to earn 10 bonus points.", completed: false },
    { id: 2, title: "Keep a Clean Sheet", description: "Have zero injured players on your team by the end of the week to earn 5 bonus points.", completed: false },
    { id: 3, title: "Top Scorer", description: "Have the highest-scoring player in your team to earn 15 bonus points.", completed: false },
  ]);

  // Placeholder function to mark challenge as complete
  const completeChallenge = (id) => {
    setChallenges(
      challenges.map(challenge =>
        challenge.id === id ? { ...challenge, completed: true } : challenge
      )
    );
  };

  return (
    <div className="challenges-page">
      <h1>Weekly Challenges</h1>
      <p>Complete these challenges to earn bonus points for your team!</p>
      <div className="challenges-list">
        {challenges.map((challenge) => (
          <div key={challenge.id} className={`challenge-card ${challenge.completed ? "completed" : ""}`}>
            <h2>{challenge.title}</h2>
            <p>{challenge.description}</p>
            <button
              className="challenge-btn"
              onClick={() => completeChallenge(challenge.id)}
              disabled={challenge.completed}
            >
              {challenge.completed ? "Completed" : "Complete Challenge"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default WeeklyChallenges;
