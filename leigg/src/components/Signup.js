import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import './Signup.css';
import Navbar from './Navbar.js';
import Footer from "./Footer.js";

function Signup() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [emptyFields, setEmptyFields] = useState({});
  const [usernameError, setUsernameError] = useState("");
  const [emailError, setEmailError] = useState("");

  const navigate = useNavigate(); // Initialize the navigate function

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

  const handleSubmit = async (e) => {
    e.preventDefault();

    const newEmptyFields = {
      username: !username,
      email: !email,
      password: !password,
      confirmPassword: !confirmPassword,
    };
    
    setEmptyFields(newEmptyFields);

    if (Object.values(newEmptyFields).some(field => field)) {
      alert("Please fill out all fields.");
      return;
    }
    
    if (!passwordError) {
      try {
        const response = await axios.post("http://127.0.0.1:5000/signup", {
          username,
          email,
          password,
        });
        
        if (response.status === 200) {
          alert("Account created successfully!");
          // Clear the form fields and error messages
          setUsername("");
          setEmail("");
          setPassword("");
          setConfirmPassword("");
          setUsernameError("");
          setEmailError("");

          // Redirect to /home after successful signup
          navigate("/");
        }
      } catch (error) {
        if (error.response) {
          const { message } = error.response.data;
          // Set specific error messages based on server response
          if (message === "Email already in use") {
            setEmailError("This email is already being used.");
            setUsernameError(""); // Clear other errors
          } else if (message === "Username already in use") {
            setUsernameError("This username is already taken.");
            setEmailError(""); // Clear other errors
          } else {
            alert("Failed to create account. Please try again.");
          }
        } else {
          console.error("There was an error creating the account:", error);
          alert("Failed to create account. Please try again.");
        }
      }
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
              className={emptyFields.username || usernameError ? "input-error" : ""}
            />
            {usernameError && <p className="error-message">{usernameError}</p>}

            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className={emptyFields.email || emailError ? "input-error" : ""}
            />
            {emailError && <p className="error-message">{emailError}</p>}

            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              placeholder="Enter your password"
              value={password}
              onChange={handlePasswordChange}
              className={emptyFields.password ? "input-error" : ""}
            />

            <label htmlFor="confirm-password">Confirm Password</label>
            <input
              type="password"
              id="confirm-password"
              placeholder="Re-enter your password"
              value={confirmPassword}
              onChange={handleConfirmPasswordChange}
              className={emptyFields.confirmPassword ? "input-error" : ""}
            />

            {passwordError && <p className="error-message">{passwordError}</p>}

            <button
              type="submit"
              className="signup-button"
            >
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
