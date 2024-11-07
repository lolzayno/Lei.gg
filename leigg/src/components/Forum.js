import React, { useState } from "react";
import './Forum.css';
import Navbar from './Navbar.js';
import Footer from "./Footer.js";

function Forum() {
  const [title, setTitle] = useState("");
  const [topic, setTopic] = useState("");
  const [content, setContent] = useState("");
  const [posts, setPosts] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    const newPost = { title, topic, content };
    setPosts([...posts, newPost]);
    setTitle("");
    setTopic("");
    setContent("");
    setIsModalOpen(false); // Close modal after submission
  };

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <div className="forum-page">
      <Navbar />
      <div className="forum-container">
        <h1>Forum</h1>
        <button className="create-post-button" onClick={openModal}>Create Post</button>
        
        {/* Post list */}
        <div className="post-list">
          {posts.length > 0 ? (
            posts.map((post, index) => (
              <div key={index} className="post-card">
                <h3>{post.title}</h3>
                <p><strong>Topic:</strong> {post.topic}</p>
                <p>{post.content}</p>
              </div>
            ))
          ) : (
            <p>No posts yet. Be the first to create one!</p>
          )}
        </div>

        {/* Modal for creating a new post */}
        {isModalOpen && (
          <div className="modal-overlay">
            <div className="modal-content">
              <h2>Create a New Post</h2>
              <form className="post-form" onSubmit={handleSubmit}>
                <label htmlFor="title">Title</label>
                <input
                  type="text"
                  id="title"
                  placeholder="Enter the post title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                />

                <label htmlFor="topic">Topic</label>
                <input
                  type="text"
                  id="topic"
                  placeholder="Enter the post topic"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                />

                <label htmlFor="content">Content</label>
                <textarea
                  id="content"
                  placeholder="Write your post content here"
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                />

                <div className="modal-buttons">
                  <button type="submit" className="submit-button">Create Post</button>
                  <button type="button" className="close-button" onClick={closeModal}>Cancel</button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
}

export default Forum;
