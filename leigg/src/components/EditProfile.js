import React, { useContext, useState, useEffect } from "react";
import { AuthContext } from "./AuthContext";
import axios from "axios";
import "./EditProfile.css";

function EditProfile() {
  const { username, login } = useContext(AuthContext);
  const [newProfilePic, setNewProfilePic] = useState(null);
  const [profilePicUrl, setProfilePicUrl] = useState("");

  // Fetch the current profile picture when the component loads
  useEffect(() => {
    const fetchProfilePic = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/get-profile-pic/${username}`, {
          responseType: 'blob',
        });
        const imageUrl = URL.createObjectURL(response.data);
        setProfilePicUrl(imageUrl);
      } catch (error) {
        console.error("Error fetching profile picture:", error);
      }
    };

    fetchProfilePic();
  }, [username]);

  const handleFileChange = (e) => {
    setNewProfilePic(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!newProfilePic) return;

    const formData = new FormData();
    formData.append("username", username);
    formData.append("profilePic", newProfilePic);

    try {
      const response = await axios.post("http://127.0.0.1:5000/update-profile-pic", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (response.status === 200) {
        const updatedProfilePicUrl = URL.createObjectURL(newProfilePic);
        setProfilePicUrl(updatedProfilePicUrl);
        login(username, updatedProfilePicUrl); // Update context with new profile picture
        alert("Profile picture updated successfully!");
      }
    } catch (error) {
      console.error("Error updating profile picture:", error);
      alert("Failed to update profile picture.");
    }
  };

  return (
    <div className="full-page-container">
      <div className="edit-profile-container">
        <h2 className="edit-profile-title">Edit Profile</h2>
        <p className="edit-profile-username">Username: {username}</p>

        <div className="current-profile">
          <h3>Current Profile Picture</h3>
          <img
            src={profilePicUrl || "https://via.placeholder.com/100"}
            alt="Current Profile"
            className="current-profile-pic"
          />
        </div>

        <form onSubmit={handleSubmit} className="edit-profile-form">
          <button type="button" className="change-pic-button">
            <label htmlFor="profilePic">Change Profile Picture</label>
          </button>
          <input
            type="file"
            id="profilePic"
            className="file-input"
            onChange={handleFileChange}
          />

          {newProfilePic && (
            <div className="new-profile-preview">
              <h4>Preview:</h4>
              <img
                src={URL.createObjectURL(newProfilePic)}
                alt="Preview"
                className="preview-pic"
              />
            </div>
          )}

          <button type="submit" className="save-changes-button">Save Changes</button>
        </form>
      </div>
    </div>
  );
}

export default EditProfile;
