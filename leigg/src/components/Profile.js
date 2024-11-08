import React from 'react';
import { useLocation, useParams, Link } from 'react-router-dom';
import './Profile.css';

function Profile() {
  const { state } = useLocation();
  const { region, ign, tag } = useParams();
  const data = state?.profileData || {};

  // Destructure data for cleaner access
  const { User, Matches, Champions } = data;

  // Check for data loading
  if (!User || !Matches || !Champions) {
    return <div>Loading profile data...</div>;
  }

  const userInfo = JSON.parse(User[2]);
  const userRankData = JSON.parse(User[3]);

  return (
    <div className="profile-page">
      {/* User Profile Section */}
      <section className="user-profile">
        <div className="profile-card">
          <img
            className="profile-icon"
            src={`https://ddragon.leagueoflegends.com/cdn/11.24.1/img/profileicon/${userInfo.profile_icon}.png`}
            alt="Profile Icon"
          />
          <h2>{userInfo.summoner_name}</h2>
          <p>Level {userInfo.summoner_level}</p>
          <div className="rank-info">
            <p><strong>{userRankData.Rank} {userRankData.Tier}</strong></p>
            <p>LP: {userRankData.LP}</p>
            <p>Win Rate: {(userRankData.WR * 100).toFixed(2)}%</p>
            <p>Games: {userRankData.Wins}/{userRankData.Games}</p>
          </div>
        </div>
      </section>

      {/* Match History Section */}
      <section className="match-history">
        <h3>Match History</h3>
        <div className="match-cards">
          {Matches.map((match, index) => (
            <div key={index} className="match-card">
              <p><strong>Match ID:</strong> {match.match_code}</p>
              <p><strong>Champion:</strong> {match.summoner_champ}</p>
              <p><strong>Lane:</strong> {match.summoner_lane}</p>
              <p><strong>Duration:</strong> {Math.floor(match.game_duration / 60)}m</p>
              <p><strong>Result:</strong> {match.result === '1' ? 'Win' : 'Loss'}</p>
              <p><strong>Items:</strong> {[match.summoner_item0, match.summoner_item1, match.summoner_item2, match.summoner_item3, match.summoner_item4, match.summoner_item5].join(', ')}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Champions Section */}
      <section className="champions">
        <h3>Champions Played</h3>
        <div className="champion-cards">
          {Champions.map((champion, index) => {
            const champData = JSON.parse(champion.champ_data);
            return (
              <div key={index} className="champion-card">
                <Link to={`/profile/${region}/${ign}/${tag}/${champion.champion}`}>
                  <p><strong>{champion.champion}</strong></p>
                </Link>
                <p>Games: {champData.summoner_GamesPlayed}</p>
                <p>Win Rate: {(champData.summoner_Winrate * 100).toFixed(2)}%</p>
                <p>KDA: {champData.summoner_KDA}</p>
                <p>Avg. Damage: {champData.summoner_TotalDmg}</p>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}

export default Profile;
