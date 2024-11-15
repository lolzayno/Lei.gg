import React, { useState, useEffect } from 'react';
import { useLocation, useParams, Link } from 'react-router-dom';
import { Bar, Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import '@fortawesome/fontawesome-free/css/all.min.css';

import './Profile.css';
import Navbar from './Navbar.js';
ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title, ChartDataLabels);
function Profile() {
  const { state } = useLocation();
  const { region, ign, tag } = useParams();
  const data = state?.profileData || {};

  
  const [activeDropdown, setActiveDropdown] = useState(null);

  const toggleDropdown = (button) => {
    setActiveDropdown((prev) => (prev === button ? null : button));
  };

  const summonerSpellMap = {
    1: "SummonerBoost",      // Cleanse
    3: "SummonerExhaust",    // Exhaust
    4: "SummonerFlash",      // Flash
    6: "SummonerHaste",      // Ghost
    7: "SummonerHeal",       // Heal
    11: "SummonerSmite",     // Smite
    12: "SummonerTeleport",  // Teleport
    13: "SummonerMana",      // Clarity
    14: "SummonerDot",       // Ignite
    21: "SummonerBarrier",   // Barrier
    30: "SummonerPoroRecall", // To the King (ARAM)
    31: "SummonerPoroThrow", // Mark
    32: "SummonerSnowball",  // Mark (ARAM)
  };

  const runePaths = {
    // Precision
    "Press the Attack": "Styles/Precision/PressTheAttack/PressTheAttack.png",
    "Fleet Footwork": "Styles/Precision/FleetFootwork/FleetFootwork.png",
    "Conqueror": "Styles/Precision/Conqueror/Conqueror.png",
    "Lethal Tempo": "Styles/Precision/LethalTempo/LethalTempoTemp.png",
  
    // Domination
    "Electrocute": "Styles/Domination/Electrocute/Electrocute.png",
    "Dark Harvest": "Styles/Domination/DarkHarvest/DarkHarvest.png",
    "Hail of Blades": "Styles/Domination/HailOfBlades/HailOfBlades.png",
    "Predator": "Styles/Domination/Predator/Predator.png",
  
    // Sorcery
    "Arcane Comet": "Styles/Sorcery/ArcaneComet/ArcaneComet.png",
    "Summon Aery": "Styles/Sorcery/SummonAery/SummonAery.png",
    "Phase Rush": "Styles/Sorcery/PhaseRush/PhaseRush.png",
  
    // Resolve
    "Grasp of the Undying": "Styles/Resolve/GraspOfTheUndying/GraspOfTheUndying.png",
    "Aftershock": "Styles/Resolve/Aftershock/Aftershock.png",
    "Guardian": "Styles/Resolve/Guardian/Guardian.png",
  
    // Inspiration
    "Glacial Augment": "Styles/Inspiration/GlacialAugment/GlacialAugment.png",
    "Unsealed Spellbook": "Styles/Inspiration/UnsealedSpellbook/UnsealedSpellbook.png",
    "First Strike": "Styles/Inspiration/FirstStrike/FirstStrike.png",
  
    // Secondary Runes (examples)
    "Cheap Shot": "Styles/Domination/CheapShot/CheapShot.png",
    "Taste of Blood": "Styles/Domination/TasteOfBlood/GreenTerror_TasteOfBlood.png",
    "Sudden Impact": "Styles/Domination/SuddenImpact/SuddenImpact.png",
    "Zombie Ward": "Styles/Domination/ZombieWard/ZombieWard.png",
    "Ghost Poro": "Styles/Domination/GhostPoro/GhostPoro.png",
    "Eyeball Collection": "Styles/Domination/EyeballCollection/EyeballCollection.png",
    "Treasure Hunter": "Styles/Domination/TreasureHunter/TreasureHunter.png",
    "Relentless Hunter": "Styles/Domination/RelentlessHunter/RelentlessHunter.png",
    "Ultimate Hunter": "Styles/Domination/UltimateHunter/UltimateHunter.png",
  
    // More examples from Sorcery
    "Nullifying Orb": "Styles/Sorcery/NullifyingOrb/Pokeshield.png",
    "Manaflow Band": "Styles/Sorcery/ManaflowBand/ManaflowBand.png",
    "Nimbus Cloak": "Styles/Sorcery/NimbusCloak/NimbusCloak.png",
    "Transcendence": "Styles/Sorcery/Transcendence/Transcendence.png",
    "Celerity": "Styles/Sorcery/Celerity/CelerityTemp.png",
    "Absolute Focus": "Styles/Sorcery/AbsoluteFocus/AbsoluteFocus.png",
    "Scorch": "Styles/Sorcery/Scorch/Scorch.png",
    "Waterwalking": "Styles/Sorcery/Waterwalking/Waterwalking.png",
    "Gathering Storm": "Styles/Sorcery/GatheringStorm/GatheringStorm.png",
  
    // Resolve Secondary Runes
    "Demolish": "Styles/Resolve/Demolish/Demolish.png",
    "Font of Life": "Styles/Resolve/FontOfLife/FontOfLife.png",
    "Shield Bash": "Styles/Resolve/ShieldBash/ShieldBash.png",
    "Conditioning": "Styles/Resolve/Conditioning/Conditioning.png",
    "Second Wind": "Styles/Resolve/SecondWind/SecondWind.png",
    "Bone Plating": "Styles/Resolve/BonePlating/BonePlating.png",
    "Overgrowth": "Styles/Resolve/Overgrowth/Overgrowth.png",
    "Revitalize": "Styles/Resolve/Revitalize/Revitalize.png",
    "Unflinching": "Styles/Resolve/Unflinching/Unflinching.png",
  
    // Inspiration Secondary Runes
    "Hextech Flashtraption": "Styles/Inspiration/HextechFlashtraption/HextechFlashtraption.png",
    "Magical Footwear": "Styles/Inspiration/MagicalFootwear/MagicalFootwear.png",
    "Biscuit Delivery": "Styles/Inspiration/BiscuitDelivery/BiscuitDelivery.png",
    "Cosmic Insight": "Styles/Inspiration/CosmicInsight/CosmicInsight.png",
    "Approach Velocity": "Styles/Inspiration/ApproachVelocity/ApproachVelocity.png",
    "Time Warp Tonic": "Styles/Inspiration/TimeWarpTonic/TimeWarpTonic.png",
    "Future's Market": "Styles/Inspiration/FuturesMarket/FuturesMarket.png",
  };
  
  
  function truncateIGN(ign) {
    return ign.length > 15 ? ign.slice(0, 15) + '...' : ign;
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
          <div className="match-cards">
            {Matches.map((match, index) => {
              const summonerData = match.summoner_data;
              // Data for the ping wheel (doughnut chart with equal segments)
              const getPingData = () => ({
                labels: [
                  'All-In', 'Assist Me', 'Total', 'Command', 'Danger', 
                  'Missing', 'Vision', 'Back', 'Hold', 'Need Vision', 
                  'On My Way', 'Push'
                ],
                datasets: [
                  {
                    // Set each data point to 1 for equal segment sizes
                    data: new Array(12).fill(1),
                    backgroundColor: [
                      '#6451fb', '#6451fb', '#6451fb', '#6451fb', '#6451fb', 
                      '#6451fb', '#6451fb', '#6451fb', '#6451fb', '#6451fb',
                      '#6451fb', '#6451fb'
                    ],
                    borderWidth: 1,
                  },
                ],
              });
              const getAbilitiesData = () => ({
                labels: ['Q', 'W', 'E', 'R', 'Spell1', 'Spell2'],
                datasets: [
                  {
                    label: 'Casts',
                    data: [
                      summonerData.summoner_Q || 0,
                      summonerData.summoner_W || 0,
                      summonerData.summoner_E || 0,
                      summonerData.summoner_R || 0,
                      summonerData.summoner_Spell1 || 0,
                      summonerData.summoner_Spell2 || 0
                    ],
                    backgroundColor: ['#4C6EFF', '#FF9A9A', '#7D94F2', '#FFD700', '#7D94F2', '#FFD700'], // Colors for each ability
                  },
                ],
              });
              const maxDamage = Math.max(
                ...["bluetop", "bluejg", "bluemid", "bluebot", "bluesup", "redtop", "redjg", "redmid", "redbot", "redsup"].map(
                  (lane) => match[`${lane}_data`][`${lane}_DMG`] || 0
                )
              );
              const maxDamageTaken = Math.max(
                ...["bluetop", "bluejg", "bluemid", "bluebot", "bluesup", "redtop", "redjg", "redmid", "redbot", "redsup"].map(
                  (lane) => match[`${lane}_data`][`${lane}_Taken`] || 0
                )
              );
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
                      <img
                        src={`https://ddragon.leagueoflegends.com/cdn/img/perk-images/${runePaths[match.summoner_rune0]}`}
                        alt="Rune Icon"
                        className="rune-icon corner-rune-icon"
                      />
                    </div>

                    <div className="summoner-spells">
                      <img 
                        src={`https://ddragon.leagueoflegends.com/cdn/14.22.1/img/spell/${summonerSpellMap[summonerData.summoner_Spell1]}.png`}
                        alt="Summoner Spell 1"
                        className="summoner-spell-icon"
                      />
                      <img 
                        src={`https://ddragon.leagueoflegends.com/cdn/14.22.1/img/spell/${summonerSpellMap[summonerData.summoner_Spell2]}.png`}
                        alt="Summoner Spell 2"
                        className="summoner-spell-icon"
                      />
                    </div>

                    <div className="items-section">
                      <div className="items">
                        {[summonerData.summoner_Item0Id, summonerData.summoner_Item1Id, summonerData.summoner_Item2Id, summonerData.summoner_Item3Id, summonerData.summoner_Item4Id, summonerData.summoner_Item5Id, summonerData.summoner_Item6Id].map((itemId, idx) => (
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
                    <div className="match-info-container">
                      <div className="result-duration">
                        <p 
                          className={`match-result ${match.result === '1' ? 'victory' : 'defeat'}`}
                          style={{ color: match.result === '1' ? '#7D94F2' : '#FF9A9A' }}
                        >
                          {match.result === '1' ? 'Victory' : 'Defeat'}
                        </p>
                        <p className="game-duration"><strong>{Math.floor(match.game_duration / 60)}:{Math.floor(match.game_duration % 60)}</strong></p>
                      </div>
                      <div className="kda-kp">
                        <p><strong>KDA:</strong> {summonerData.summoner_Kills}/{summonerData.summoner_Deaths}/{summonerData.summoner_Assists || 0}</p>
                        <p><strong>KP:</strong> {summonerData.summoner_KP}</p>
                      </div>
                      <div className="farm-solo-kills">
                        <p><strong>Farm:</strong> {summonerData.summoner_Minions} ({(summonerData.summoner_Minions / Math.floor(match.game_duration / 60)).toFixed(1)})</p>
                        <p><strong>Solo Kills:</strong> {summonerData.summoner_SoloKill}</p>
                      </div>
                    </div>
                  </div>
                  <div className="team-champions">
                    <div className="champions-columns">
                      <div className="blue-side-column">
                        {["bluetop", "bluejg", "bluemid", "bluebot", "bluesup"].map((lane) => {
                          const rank = match[`${lane}_data`][`${lane}_Rank`];
                          const tier = match[`${lane}_data`][`${lane}_Tier`];
                          const lp = match[`${lane}_data`][`${lane}_lp`];
                          const damagePhysical = match[`${lane}_data`][`${lane}_PhysicalDMG`] || 0;
                          const damageMagic = match[`${lane}_data`][`${lane}_MagicDMG`] || 0;
                          const damageTrue = match[`${lane}_data`][`${lane}_TrueDMG`] || 0;
                          const totalDamage = damagePhysical + damageMagic + damageTrue;
                          const damagePercent = (totalDamage / maxDamage) * 100;
                          const damagePhysicalTaken = match[`${lane}_data`][`${lane}_PhysicalTaken`] || 0;
                          const damageMagicTaken = match[`${lane}_data`][`${lane}_MagicTaken`] || 0;
                          const damageTrueTaken = match[`${lane}_data`][`${lane}_TrueTaken`] || 0;
                          const totalDamageTaken = damagePhysicalTaken + damageMagicTaken + damageTrueTaken;
                          const damagePercentTaken = (totalDamageTaken / maxDamageTaken) * 100;
                          return (
                            <div className="lane" key={lane}>
                              <span className="blue-side-ign">{truncateIGN(match[`${lane}_data`][`${lane}_IGN`])}</span>
                              <div className="damage-bar-wrapper">
                                <div className="damage-bar-container">
                                  <div
                                    className="damage-bar red-bar"
                                    style={{ width: `${(damagePhysical / totalDamage) * damagePercent}%` }}
                                    data-tooltip={`${damagePhysical} Physical Damage`}
                                  />
                                  <div
                                    className="damage-bar blue-bar"
                                    style={{ width: `${(damageMagic / totalDamage) * damagePercent}%` }}
                                    data-tooltip={`${damageMagic} Magic Damage`}
                                  />
                                  <div
                                    className="damage-bar white-bar"
                                    style={{ width: `${(damageTrue / totalDamage) * damagePercent}%` }}
                                    data-tooltip={`${damageTrue} True Damage`}
                                  />
                                </div>
                                <div className="total-damage">{totalDamage}</div>
                                <div className="damage-bar-container">
                                  <div
                                    className="damage-bar red-bar"
                                    style={{ width: `${(damagePhysicalTaken / totalDamageTaken) * damagePercentTaken}%` }}
                                    data-tooltip={`${damagePhysicalTaken} Physical Damage`}
                                  />
                                  <div
                                    className="damage-bar blue-bar"
                                    style={{ width: `${(damageMagicTaken / totalDamageTaken) * damagePercentTaken}%` }}
                                    data-tooltip={`${damageMagicTaken} Magic Damage`}
                                  />
                                  <div
                                    className="damage-bar white-bar"
                                    style={{ width: `${(damageTrueTaken / totalDamageTaken) * damagePercentTaken}%` }}
                                    data-tooltip={`${damageTrueTaken} True Damage`}
                                  />
                                </div>
                                <div className="total-damage">{totalDamageTaken}</div>
                              </div>
                              
                              <div className="rank-icon-container" data-tooltip={`${lp} LP`}>
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
                          const lp = match[`${lane}_data`][`${lane}_lp`];
                          const damagePhysical = match[`${lane}_data`][`${lane}_PhysicalDMG`] || 0;
                          const damageMagic = match[`${lane}_data`][`${lane}_MagicDMG`] || 0;
                          const damageTrue = match[`${lane}_data`][`${lane}_TrueDMG`] || 0;
                          const totalDamage = damagePhysical + damageMagic + damageTrue;
                          const damagePercent = (totalDamage / maxDamage) * 100;
                          const damagePhysicalTaken = match[`${lane}_data`][`${lane}_PhysicalTaken`] || 0;
                          const damageMagicTaken = match[`${lane}_data`][`${lane}_MagicTaken`] || 0;
                          const damageTrueTaken = match[`${lane}_data`][`${lane}_TrueTaken`] || 0;
                          const totalDamageTaken = damagePhysicalTaken + damageMagicTaken + damageTrueTaken;
                          const damagePercentTaken = (totalDamageTaken / maxDamageTaken) * 100;

                          return (
                            <div className="lane" key={lane}>
                              <img src={`https://ddragon.leagueoflegends.com/cdn/14.22.1/img/champion/${match[`${lane}_champ`]}.png`} alt={`Red ${lane}`} />
                              <div className="rank-icon-container" data-tooltip={`${lp} LP`}>
                                <img 
                                  src={`https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-mini-crests/${rank.toLowerCase()}.svg`}
                                  alt={`${rank} rank icon`}
                                  className="rank-icon blue-rank-icon"
                                />
                                <span className="rank-tier">{tier}</span>
                              </div>
                              <div className="damage-bar-wrapper">
                                <div className="damage-bar-container">
                                  <div
                                    className="damage-bar red-bar"
                                    style={{ width: `${(damagePhysical / totalDamage) * damagePercent}%` }}
                                    data-tooltip={`${damagePhysical} Physical Damage`}
                                  />
                                  <div
                                    className="damage-bar blue-bar"
                                    style={{ width: `${(damageMagic / totalDamage) * damagePercent}%` }}
                                    data-tooltip={`${damageMagic} Magic Damage`}
                                  />
                                  <div
                                    className="damage-bar white-bar"
                                    style={{ width: `${(damageTrue / totalDamage) * damagePercent}%` }}
                                    data-tooltip={`${damageTrue} True Damage`}
                                  />
                                </div>
                                <div className="total-damage">{totalDamage}</div>
                                <div className="damage-bar-container">
                                  <div
                                    className="damage-bar red-bar"
                                    style={{ width: `${(damagePhysicalTaken / totalDamageTaken) * damagePercentTaken}%` }}
                                    data-tooltip={`${damagePhysicalTaken} Physical Damage`}
                                  />
                                  <div
                                    className="damage-bar blue-bar"
                                    style={{ width: `${(damageMagicTaken / totalDamageTaken) * damagePercentTaken}%` }}
                                    data-tooltip={`${damageMagicTaken} Magic Damage`}
                                  />
                                  <div
                                    className="damage-bar white-bar"
                                    style={{ width: `${(damageTrueTaken / totalDamageTaken) * damagePercentTaken}%` }}
                                    data-tooltip={`${damageTrueTaken} True Damage`}
                                  />
                                </div>
                                <div className="total-damage">{totalDamageTaken}</div>
                              </div>
                              <span className="red-side-ign">{truncateIGN(match[`${lane}_data`][`${lane}_IGN`])}</span>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  </div>
                  <div className="button-group">
                    <button
                      onClick={() => toggleDropdown('Rune')}
                      className={`icon-button ${activeDropdown === 'Rune' ? 'active' : ''}`}
                    >
                      <i class="fa-solid fa-scroll"></i>
                    </button>
                    <button
                      onClick={() => toggleDropdown('Abilities')}
                      className={`icon-button ${activeDropdown === 'Abilities' ? 'active' : ''}`}
                    >
                      <i class="fa-solid fa-wand-sparkles"></i>
                    </button>
                    <button
                      onClick={() => toggleDropdown('Objective')}
                      className={`icon-button ${activeDropdown === 'Objective' ? 'active' : ''}`}
                    >
                      <i class="fa-solid fa-dragon"></i>
                    </button>
                    <button
                      onClick={() => toggleDropdown('Ping')}
                      className={`icon-button ${activeDropdown === 'Ping' ? 'active' : ''}`}
                    >
                      <i className="fas fa-bell"></i>
                    </button>
                    <button
                      onClick={() => toggleDropdown('Tower')}
                      className={`icon-button ${activeDropdown === 'Tower' ? 'active' : ''}`}
                    >
                      <i class="fa-solid fa-chess-rook"></i>
                    </button>
                    <button
                      onClick={() => toggleDropdown('Vision')}
                      className={`icon-button ${activeDropdown === 'Vision' ? 'active' : ''}`}
                    >
                      <i class="fa-solid fa-eye"></i>
                    </button>
                    <button
                      onClick={() => toggleDropdown('Support')}
                      className={`icon-button ${activeDropdown === 'Support' ? 'active' : ''}`}
                    >
                      <i class="fa-solid fa-heart-pulse"></i>
                    </button>
                  </div>


                  {/* Dropdown content for each button */}
                  {activeDropdown === 'Rune' && (
                    <div className="dropdown-content">
                      {/* Display rune-related data */}
                      <p>Primary Rune: {summonerData.summoner_Rune01}</p>
                      <p>Secondary Rune: {summonerData.summoner_Rune02}</p>
                    </div>
                  )}
                  {activeDropdown === 'Abilities' && (
                  <div className="dropdown-content">
                    <Bar data={getAbilitiesData()} options={{
                      responsive: true,
                      plugins: {
                        legend: {
                          display: false,
                        },
                        tooltip: {
                          callbacks: {
                            label: function (tooltipItem) {
                              return ` ${tooltipItem.formattedValue} casts`;
                            },
                          },
                        },
                      },
                      scales: {
                        y: {
                          beginAtZero: true,
                          title: {
                            display: true,
                            text: 'Casts',
                          },
                        },
                      },
                    }} />
                  </div>
                )}
                  {activeDropdown === 'Objective' && (
                    <div className="dropdown-content">
                      {/* Display objective damage data */}
                      <p>Damage to Objectives: {summonerData.summoner_DamageObj}</p>
                      <p>Damage to Turrets: {summonerData.summoner_DamageBuilding}</p>
                    </div>
                  )}
                  {/* Dropdown content for ping data with doughnut chart */}
                  {activeDropdown === 'Ping' && (
                  <div className="dropdown-content">
                    <Doughnut 
                    data={getPingData()} 
                    width={265}  
                    height={265} 
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      cutout: '25%',  // Adjust this value to make the hole smaller (e.g., '30%' for an even smaller hole)
                      plugins: {
                        legend: { display: false },
                        tooltip: {
                          callbacks: {
                            label: function (tooltipItem) {
                              const actualCounts = [
                                summonerData.summoner_AllInPings || 0,
                                summonerData.summoner_AssistMePings || 0,
                                summonerData.summoner_Pings || 0,
                                summonerData.summoner_CommandPings || 0,
                                summonerData.summoner_DangerPing || 0,
                                summonerData.summoner_MissingPing || 0,
                                summonerData.summoner_VisionPing || 0,
                                summonerData.summoner_BackPing || 0,
                                summonerData.summoner_HoldPing || 0,
                                summonerData.summoner_NeedVisionPing || 0,
                                summonerData.summoner_OnMyWayPing || 0,
                                summonerData.summoner_PushPings || 0,
                              ];
                              return `${tooltipItem.label}: ${actualCounts[tooltipItem.dataIndex]} uses`;
                            },
                          },
                        },
                        datalabels: {
                          display: true,
                          color: 'black',
                          formatter: (value, ctx) => {
                            const actualCounts = [
                              summonerData.summoner_AllInPings || 0,
                              summonerData.summoner_AssistMePings || 0,
                              summonerData.summoner_Pings || 0,
                              summonerData.summoner_CommandPings || 0,
                              summonerData.summoner_DangerPing || 0,
                              summonerData.summoner_MissingPing || 0,
                              summonerData.summoner_VisionPing || 0,
                              summonerData.summoner_BackPing || 0,
                              summonerData.summoner_HoldPing || 0,
                              summonerData.summoner_NeedVisionPing || 0,
                              summonerData.summoner_OnMyWayPing || 0,
                              summonerData.summoner_PushPings || 0,
                            ];
                            let label = ctx.chart.data.labels[ctx.dataIndex];
                            return `${label}\n${actualCounts[ctx.dataIndex]}`;
                          },
                        },
                      },
                      rotation: -90,
                      circumference: 360,
                    }}
                  />

                  </div>
                )}

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
