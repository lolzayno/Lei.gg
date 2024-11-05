import React from "react";
import "./Navbar.css";
import { Button } from 'primereact/button';
import 'primeicons/primeicons.css';
function Navbar() {
  const handleClickHome = () => {
    window.location.href = 'http://localhost:3000/'; // Navigate to the homepage
  }
  const handleClickBot = () => {
    window.location.href = 'https://chatgpt.com/g/g-9WhJXAiXP-league-of-legends-advisor'; // Navigate to the homepage
  }
  const handleClickCoach = () => {
    window.location.href = 'http://localhost:3000/coaching'; // Navigate to the homepage
  }
  const handleClickForum = () => {
    window.location.href = 'http://localhost:3000/forum'; // Navigate to the homepage
  }
  const handleClickUser = () => {
    window.location.href = 'http://localhost:3000/login'; // Navigate to the homepage
  }
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
        <Button 
        icon="pi pi-user" 
        className="custom-button" 
        onClick={handleClickUser} 
        aria-label="Login"
        />
      </div>
    </nav>
  );
}

export default Navbar;
