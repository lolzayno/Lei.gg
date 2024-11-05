import './Search.css';
import React, { useState } from "react";
import Select from 'react-select';
const countries = [
    { label: 'North America', value: 'NA' },
    { label: 'Europe West', value: 'EUW' },
    { label: 'Europe Nordic & East', value: 'EUNE' },
    { label: 'Oceania', value: 'OCE' },
    { label: 'Russia', value: 'RU' },
    { label: 'Turkey', value: 'TR' },
    { label: 'Brazil', value: 'BR' },
    { label: 'Latin America North', value: 'LAN' },
    { label: 'Latin America South', value: 'LAS' },
    { label: 'Japan', value: 'JP' },
    { label: 'Taiwan', value: 'TW' },
    { label: 'Singapore, Malaysia, Indonesia', value: 'SEA' },
    { label: 'Thailand', value: 'TH' },
    { label: 'Philippines', value: 'PH' },
    { label: 'Middle East', value: 'ME' }
];

function Search() {
    const [summonerName, setSummonerName] = useState("");
    const [region, setRegion] = useState(countries[0]);

    const handleSearch = () => {
      alert(`Searching for summoner: ${summonerName} in region: ${region.label}`);
    };

    return (
      <div className="search-container">
        <div className="search-pill">
          <div className="input-wrapper">
            <label className="input-label" htmlFor="region-select">Region</label>
            <Select
            id="region-select"
            options={countries}
            value={region}
            onChange={setRegion}
            className="custom-select"
            classNamePrefix="custom"
            styles={{
                control: (base) => ({
                ...base,
                border: '2px solid #6451fb',
                borderRadius: '50px',
                padding: '0 10px', // Consistent padding
                fontSize: '1rem',
                color: '#6451fb',
                backgroundColor: '#f9f8ff',
                width: '300px',  // Match summoner input width
                cursor: 'pointer',
                '&:hover': {
                    borderColor: '#483d8b', // Darker border on hover
                    backgroundColor: '#d0c4ff', // Set hover background color
                },
                }),
                singleValue: (base) => ({
                ...base,
                color: '#6451fb',
                }),
                placeholder: (base) => ({
                ...base,
                color: '#8275fd',
                }),
                dropdownIndicator: (base) => ({
                ...base,
                color: '#6451fb',
                '&:hover': { color: '#483d8b' },
                }),
                menu: (base) => ({
                ...base,
                backgroundColor: '#f9f8ff',
                border: '1px solid #6451fb',
                borderRadius: '10px',
                marginTop: '5px',
                }),
                option: (base, state) => ({
                ...base,
                backgroundColor: state.isFocused ? '#d0c4ff' : '#f9f8ff',
                color: state.isFocused ? '#483d8b' : '#6451fb',
                padding: '10px',
                cursor: 'pointer',
                }),
            }}
            components={{
                IndicatorSeparator: () => null,
            }}
            placeholder="Select Region"
            />
          </div>
          <div className="input-wrapper">
            <label className="input-label" htmlFor="summoner-name">Summoner</label>
            <input
              id="summoner-name"
              type="text"
              placeholder="Summoner Name (e.g., Zayno#NA1)"
              value={summonerName}
              onChange={(e) => setSummonerName(e.target.value)}
              className="search-input"
            />
          </div>
          <button onClick={handleSearch} className="search-button">
            Search
          </button>
        </div>
      </div>
    );
}

export default Search;
