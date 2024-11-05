import React, { useState } from "react";
import './Forgot.css';
import Navbar from './Navbar.js';
import Footer from "./Footer.js";

function Forgot() {
  const [email, setEmail] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Password reset link sent to " + email);
    // Here you would typically call a backend API to handle the password reset request
  };

  return (
    <div>
        <Navbar />
        <div className="forgot-page">
        <div className="forgot-container">
            <h2>Forgot Your Password?</h2>
            <p>Please enter the email associated with your account, and we'll send a password reset link.</p>
            <form className="forgot-form" onSubmit={handleSubmit}>
            <label htmlFor="email">Email</label>
            <input
                type="email"
                id="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
            />
            <button type="submit" className="forgot-button">Send Reset Link</button>
            </form>
        </div>
        </div>
        <Footer />
    </div>
  );
}

export default Forgot;
