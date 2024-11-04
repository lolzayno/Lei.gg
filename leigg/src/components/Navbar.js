import React from "react";
import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="nav-left">
        <a href="/" className="nav-link">
          Home
        </a>
      </div>
      <div className="nav-right">
        <a href="/chatbot" className="nav-link">
          Chatbot
        </a>
      </div>
    </nav>
  );
}

export default Navbar;
