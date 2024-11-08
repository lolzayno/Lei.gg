import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import './Champion.css';

function Champion() {
  const { region, ign, tag, champion } = useParams();
  const [champData, setChampData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch champion data from the backend
    fetch(`http://localhost:5000/profile/${region}/${ign}/${tag}/${champion}`)
      .then(response => response.json())
      .then(data => {
        setChampData(data); // Set champion data
        setLoading(false); // Set loading to false once data is received
      })
      .catch(error => {
        console.error('Error fetching champion data:', error);
        setLoading(false);
      });
  }, [region, ign, tag, champion]);

  // Display loading message until data is fetched
  if (loading) {
    return <div>Loading champion data...</div>;
  }

  // Handle the case where champData is still null (e.g., in case of an error)
  if (!champData) {
    return <div>Error loading champion data. Please try again later.</div>;
  }

  const champDetails = JSON.parse(champData.champ_data);
  return (
    <div className="champion-page">
      <h2>{champion} Details</h2>
      <div className="champion-stats">
        <p><strong>Games Played:</strong> {champDetails.summoner_GamesPlayed}</p>
        <p><strong>Win Rate:</strong> {(champDetails.summoner_Winrate * 100).toFixed(2)}%</p>
        <p><strong>KDA:</strong> {champDetails.summoner_KDA}</p>
        <p><strong>Average Damage:</strong> {champDetails.summoner_TotalDmg}</p>
        <p><strong>Average CS:</strong> {champDetails.summoner_Minions}</p>
        <p><strong>Average Gold Earned:</strong> {champDetails.summoner_Exp}</p>
        <p><strong>Damage Dealt to Objectives:</strong> {champDetails.summoner_DamageObj}</p>
      </div>
    </div>
  );
}

export default Champion;
