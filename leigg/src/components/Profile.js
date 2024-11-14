import React, { useState, useEffect } from 'react';
import { useLocation, useParams, Link } from 'react-router-dom';
import './Profile.css';
import Navbar from './Navbar.js';

function Profile() {
  const { state } = useLocation();
  const { region, ign, tag } = useParams();
  const data = state?.profileData || {};

  const [itemMapping, setItemMapping] = useState({});
  
  function truncateIGN(ign) {
    return ign.length > 10 ? ign.slice(0, 10) + '...' : ign;
  }


  const { User, Matches, Champions } = data;

  if (!User || !Matches || !Champions) {
    return <div>Loading profile data...</div>;
  }

  const userInfo = JSON.parse(User[2]);
  const userRankData = JSON.parse(User[3]);

  return (
    <div>
      <Navbar />
      <div className="profile-page">
        <section className="user-profile">
          <div className="profile-card">
            <img
              className="profile-icon"
              src={`https://ddragon.leagueoflegends.com/cdn/14.22.1/img/profileicon/${userInfo.profile_icon}.png`}
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

        <section className="match-history">
          <h3>Match History</h3>
          <div className="match-cards">
            {Matches.map((match, index) => {
              const summonerData = match.summoner_data;

              return (
                <div 
                  key={index} 
                  className={`match-card ${match.result === '1' ? 'win' : 'loss'}`} 
                  style={{
                    borderLeft: `5px solid ${match.result === '1' ? '#7D94F2' : '#FF9A9A'}`,
                  }}
                >
                  <div className="match-header">
                    <div className="champion-icon-container">
                      <img
                        src={`https://ddragon.leagueoflegends.com/cdn/14.22.1/img/champion/${match.summoner_champ}.png`}
                        alt={`${match.summoner_champ} icon`}
                        className="champion-icon user-champion-icon"
                      />
                      <span className="champion-level">{summonerData.summoner_Level}</span>
                    </div>
                    <div className="items-section">
                      <div className="items">
                        {[summonerData.summoner_Item0Id, summonerData.summoner_Item1Id, summonerData.summoner_Item2Id, summonerData.summoner_Item3Id, summonerData.summoner_Item4Id, summonerData.summoner_Item5Id].map((itemId, idx) => (
                          itemId ? (
                            <img 
                              key={idx} 
                              src={`https://ddragon.leagueoflegends.com/cdn/14.22.1/img/item/${itemId}.png`} 
                              alt={`Item ${itemId}`} 
                              className="item-icon" 
                            />
                            
                          ) : null
                        ))}
                      </div>
                    </div>
                  </div>
                  <div>
                      <p 
                        className={`match-result ${match.result === '1' ? 'victory' : 'defeat'}`}
                        style={{ color: match.result === '1' ? '#7D94F2' : '#FF9A9A' }}
                      >
                        {match.result === '1' ? 'Victory' : 'Defeat'}
                      </p>
                    </div>
                  <p><strong>{Math.floor(match.game_duration / 60)} min & {Math.floor(match.game_duration % 60)} sec</strong></p>
                  <div className="kda">
                    <p><strong>KDA:</strong> {summonerData.summoner_Kills}/{summonerData.summoner_Deaths}/{summonerData.summoner_Assists || 0}</p>
                  </div>
                  
                  <div className="team-champions">
                    <div className="champions-columns">
                      <div className="blue-side-column">
                        {["bluetop", "bluejg", "bluemid", "bluebot", "bluesup"].map((lane) => {
                          const rank = match[`${lane}_data`][`${lane}_Rank`];
                          const tier = match[`${lane}_data`][`${lane}_Tier`];
                          return (
                            <div className="lane" key={lane}>
                              <span className="blue-side-ign">{truncateIGN(match[`${lane}_data`][`${lane}_IGN`])}</span>
                              <div className="rank-icon-container">
                                <img 
                                  src={`https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-mini-crests/${rank.toLowerCase()}.svg`}
                                  alt={`${rank} rank icon`}
                                  className="rank-icon blue-rank-icon"
                                />
                                <span className="rank-tier">{tier}</span>
                              </div>
                              <img src={`https://ddragon.leagueoflegends.com/cdn/14.22.1/img/champion/${match[`${lane}_champ`]}.png`} alt={`Blue ${lane}`} />
                            </div>
                          );
                        })}
                      </div>

                      <div className="red-side-column">
                        {["redtop", "redjg", "redmid", "redbot", "redsup"].map((lane) => {
                          const rank = match[`${lane}_data`][`${lane}_Rank`];
                          const tier = match[`${lane}_data`][`${lane}_Tier`];
                          return (
                            <div className="lane" key={lane}>
                              <img src={`https://ddragon.leagueoflegends.com/cdn/14.22.1/img/champion/${match[`${lane}_champ`]}.png`} alt={`Red ${lane}`} />
                              <div className="rank-icon-container">
                                <img 
                                  src={`https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-mini-crests/${rank.toLowerCase()}.svg`}
                                  alt={`${rank} rank icon`}
                                  className="rank-icon red-rank-icon"
                                />
                                <span className="rank-tier">{tier}</span>
                              </div>
                              <span className="red-side-ign">{truncateIGN(match[`${lane}_data`][`${lane}_IGN`])}</span>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  </div>

                </div>
              );
            })}
          </div>
        </section>
      </div>
    </div>
  );
}

export default Profile;
