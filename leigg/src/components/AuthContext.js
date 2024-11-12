import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [username, setUsername] = useState(localStorage.getItem('username') || null);
  const [profilePic, setProfilePic] = useState(localStorage.getItem('profilePic') || null);

  const login = async (username, profilePicUrl) => {
    setUsername(username);
    setProfilePic(profilePicUrl);
    localStorage.setItem('username', username);
    localStorage.setItem('profilePic', profilePicUrl);
  };

  const logout = () => {
    setUsername(null);
    setProfilePic(null);
    localStorage.removeItem('username');
    localStorage.removeItem('profilePic');
  };

  // Fetch profile picture if username exists but no profilePic is set
  useEffect(() => {
    const fetchProfilePic = async () => {
      if (username && !profilePic) {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/get-profile-pic/${username}`, {
            responseType: 'blob'
          });
          const profilePicUrl = URL.createObjectURL(response.data);
          setProfilePic(profilePicUrl);
          localStorage.setItem('profilePic', profilePicUrl);
        } catch (error) {
          console.error("Error fetching profile picture:", error);
        }
      }
    };
    fetchProfilePic();
  }, [username, profilePic]);

  return (
    <AuthContext.Provider value={{ username, profilePic, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
