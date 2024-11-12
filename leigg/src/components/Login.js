import React, { useState, useContext } from "react";
import axios from "axios";
import { useNavigate, useLocation } from "react-router-dom";
import { AuthContext } from "./AuthContext";
import './Login.css';
import Navbar from './Navbar';
import Footer from "./Footer";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); // Clear previous errors

    try {
      const response = await axios.post("http://127.0.0.1:5000/login", {
        username,
        password,
      });

      if (response.status === 200) {
        login(username); // Set username in context
        // Redirect to the previous page or home if no previous page is stored
        const redirectTo = location.state?.from || "/";
        navigate(redirectTo);
      }
    } catch (error) {
      if (error.response && error.response.status === 400) {
        setError("Incorrect username or password. Please try again.");
      } else {
        console.error("There was an error logging in:", error);
        setError("An unexpected error occurred. Please try again.");
      }
    }
  };

  return (
    <div>
      <Navbar />
      <div className="login-page">
        <div className="login-container">
          <h2>Welcome Back</h2>
          <form className="login-form" onSubmit={handleSubmit}>
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />

            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            {error && <p className="error-message">{error}</p>}

            <button type="submit" className="login-button">
              Login
            </button>
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
