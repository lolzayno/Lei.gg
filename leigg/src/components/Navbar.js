import React, { useContext, useState, useEffect, useRef } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./Navbar.css";
import { Button } from 'primereact/button';
import 'primeicons/primeicons.css';
import { AuthContext } from './AuthContext';

function Navbar() {
  const { username, profilePic, logout } = useContext(AuthContext);
  const [isDropdownVisible, setIsDropdownVisible] = useState(false);
  const dropdownRef = useRef(null);
  const navigate = useNavigate();
  const location = useLocation();

  const handleClickHome = () => {
    navigate('/');
  };

  const handleClickBot = () => {
    window.location.href = 'https://chatgpt.com/g/g-9WhJXAiXP-league-of-legends-advisor';
  };

  const handleClickCoach = () => {
    navigate('/coaching');
  };

  const handleClickForum = () => {
    navigate('/forum');
  };

  const handleClickUser = () => {
    navigate('/login', { state: { from: location.pathname } });
  };

  const handleProfileClick = () => {
    navigate('/edit-profile');
  };

  const toggleDropdown = () => {
    setIsDropdownVisible((prev) => !prev);
  };

  // Close dropdown if clicking outside of it
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDropdownVisible(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <nav className="navbar">
      <div className="nav-left">
        <Button 
          icon="pi pi-home" 
          className="custom-button" 
          onClick={handleClickHome} 
          aria-label="Home"
        />
      </div>
      <div className="nav-right">
        <Button 
          icon="pi pi-comments" 
          className="custom-button" 
          onClick={handleClickForum} 
          aria-label="Forum"
        />
        <Button 
          icon="pi pi-graduation-cap" 
          className="custom-button" 
          onClick={handleClickCoach} 
          aria-label="Coach"
        />
        <Button 
          icon="pi pi-microchip-ai" 
          className="custom-button" 
          onClick={handleClickBot} 
          aria-label="AI"
        />
        {username ? (
          <div className="profile-container" ref={dropdownRef}>
            <img 
              src={profilePic || "https://via.placeholder.com/40"} 
              alt="Profile" 
              className="profile-pic"
              onClick={toggleDropdown} // Toggle dropdown on click
            />
            {isDropdownVisible && (
              <div className="dropdown-menu">
                <button onClick={handleProfileClick} className="dropdown-item">Profile</button>
                <button onClick={logout} className="dropdown-item">Sign Out</button>
              </div>
            )}
          </div>
        ) : (
          <Button 
            icon="pi pi-user" 
            className="custom-button" 
            onClick={handleClickUser} 
            aria-label="Login"
          />
        )}
      </div>
    </nav>
  );
}

export default Navbar;
