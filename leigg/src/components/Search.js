import './Search.css';
import React, { useState } from "react";
import Select from 'react-select';
import { useNavigate } from 'react-router-dom';

const countries = [
    { label: 'North America', value: 'NA1' },
    { label: 'Europe West', value: 'EUW1' },
    { label: 'Europe Nordic & East', value: 'EUN1' },
    { label: 'Oceania', value: 'OCE' },
    { label: 'Russia', value: 'RU' },
    { label: 'Turkey', value: 'TR1' },
    { label: 'Brazil', value: 'BR1' },
    { label: 'Latin America North', value: 'LAN' },
    { label: 'Latin America South', value: 'LAS' },
    { label: 'Japan', value: 'JP1' },
    { label: 'Taiwan', value: 'TW' },
    { label: 'Singapore, Malaysia, Indonesia', value: 'SEA' },
    { label: 'Thailand', value: 'TH' },
    { label: 'Philippines', value: 'PH' },
    { label: 'Middle East', value: 'ME' }
];

function Search() {
    const [summonerName, setSummonerName] = useState("");
    const [region, setRegion] = useState(countries[0]);
    const navigate = useNavigate();

    const handleSearch = () => {
        // Split summonerName into ign and tag
        const [ign, tag] = summonerName.split("#");

        fetch('http://localhost:5000/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                summonerName: summonerName,
                region: region.value
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data); // Verify data structure here
            // Pass data as state in navigate
            navigate(`/profile/${region.value}/${ign}/${tag}`, { state: { profileData: data } });
        })
        .catch(error => {
            console.error('Error:', error);
        });
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
                                padding: '0 10px',
                                fontSize: '1rem',
                                color: '#6451fb',
                                backgroundColor: '#f9f8ff',
                                width: '300px',
                                cursor: 'pointer',
                                '&:hover': {
                                    borderColor: '#483d8b',
                                    backgroundColor: '#d0c4ff',
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
