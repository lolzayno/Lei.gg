import React from "react";
import './Coach.css';
import Navbar from './Navbar.js';
import Footer from "./Footer.js";

function Coach() {
  const coaches = [
    {
      ign: 'Zayno',
      lane: 'Mid',
      champion: 'Ziggs',
      rank: 'Challenger',
    },
    {
      ign: "Gemi",
      lane: 'Top',
      champion: 'Poppy',
      rank: 'Challenger'
    }
  ];

  return (
    <div className="coach-page">
      <Navbar />
      <div className="coach-container">
        <h2>Select Your Coach</h2>
        <div className="coach-cards">
          {coaches.map((coach, index) => (
            <div key={index} className="coach-card">
              <h3>{coach.ign}</h3>
              <p><strong>Lane Specialty:</strong> {coach.lane}</p>
              <p><strong>Champion Specialty:</strong> {coach.champion}</p>
              <p><strong>Peak Rank:</strong> {coach.rank}</p>
              <button className="select-button">Select Coach</button>
            </div>
          ))}
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default Coach;
