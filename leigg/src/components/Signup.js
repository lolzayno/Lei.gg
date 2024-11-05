import React, { useState } from "react";
import './Signup.css';
import Navbar from './Navbar.js';
import Footer from "./Footer.js";

function Signup() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
    if (confirmPassword && e.target.value !== confirmPassword) {
      setPasswordError("Passwords do not match");
    } else {
      setPasswordError("");
    }
  };

  const handleConfirmPasswordChange = (e) => {
    setConfirmPassword(e.target.value);
    if (password && e.target.value !== password) {
      setPasswordError("Passwords do not match");
    } else {
      setPasswordError("");
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!passwordError) {
      alert("Account created successfully!");
      // Perform signup logic here (e.g., send data to an API)
    }
  };

  return (
    <div>
        <Navbar />
        <div className="signup-page">
        <div className="signup-container">
            <h2>Create Your Account</h2>
            <form className="signup-form" onSubmit={handleSubmit}>
            <label htmlFor="username">Username</label>
            <input
                type="text"
                id="username"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />

            <label htmlFor="email">Email</label>
            <input
                type="email"
                id="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />

            <label htmlFor="password">Password</label>
            <input
                type="password"
                id="password"
                placeholder="Enter your password"
                value={password}
                onChange={handlePasswordChange}
            />

            <label htmlFor="confirm-password">Confirm Password</label>
            <input
                type="password"
                id="confirm-password"
                placeholder="Re-enter your password"
                value={confirmPassword}
                onChange={handleConfirmPasswordChange}
            />

            {passwordError && <p className="error-message">{passwordError}</p>}

            <button type="submit" className="signup-button" disabled={!!passwordError}>
                Sign Up
            </button>
            </form>
        </div>
        </div>
        <Footer />
    </div>
  );
}

export default Signup;
