import React from "react";
import './Login.css';
import Navbar from './Navbar.js';
import Footer from "./Footer.js";

function Login() {
  return (
    <div>
      <Navbar />
      <div className="login-page">
        <div className="login-container">
          <h2>Welcome Back</h2>
          <form className="login-form">
            <label htmlFor="username">Username</label>
            <input type="text" id="username" placeholder="Enter your username" />

            <label htmlFor="password">Password</label>
            <input type="password" id="password" placeholder="Enter your password" />

            <button type="submit" className="login-button">Login</button>

            <div className="login-links">
              <a href="/signup">Sign Up</a>
              <span>|</span>
              <a href="/forgot-password">Forgot Password?</a>
            </div>
          </form>
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default Login;
