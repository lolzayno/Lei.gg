import React, { useState } from "react";
import './Forum.css';
import Navbar from './Navbar.js';
import Footer from "./Footer.js";

function Forum() {
  const [title, setTitle] = useState("");
  const [topic, setTopic] = useState("");
  const [content, setContent] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Post created: \nTitle: ${title}\nTopic: ${topic}\nContent: ${content}`);
    setTitle("");
    setTopic("");
    setContent("");
  };

  return (
    <div className="forum-page">
      <Navbar />
      <div className="forum-container">
        <h1>Forum</h1>
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

          <button type="submit" className="submit-button">Create Post</button>
        </form>
      </div>
      <Footer />
    </div>
  );
}

export default Forum;
