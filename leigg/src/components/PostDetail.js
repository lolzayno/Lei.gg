import React, { useState } from "react";
import { useParams } from "react-router-dom";
import './PostDetail.css';
import Navbar from './Navbar.js';
import Footer from "./Footer.js";

function PostDetail({ posts }) {
  const { postId } = useParams();
  const post = posts.find((p) => p.id === parseInt(postId));
  const [replies, setReplies] = useState([]);
  const [replyContent, setReplyContent] = useState("");

  const handleReplySubmit = (e) => {
    e.preventDefault();
    setReplies([...replies, replyContent]);
    setReplyContent("");
  };

  if (!post) return <p>Post not found</p>;

  return (
    <div className="post-detail-page">
      <Navbar />
      <div className="post-detail-container">
        <h2>{post.title}</h2>
        <p><strong>Topic:</strong> {post.topic}</p>
        <p>{post.content}</p>

        <div className="replies-section">
          <h3>Replies</h3>
          {replies.length > 0 ? (
            replies.map((reply, index) => (
              <div key={index} className="reply">
                <p>{reply}</p>
              </div>
            ))
          ) : (
            <p>No replies yet. Be the first to reply!</p>
          )}
        </div>

        <form className="reply-form" onSubmit={handleReplySubmit}>
          <textarea
            placeholder="Write your reply here"
            value={replyContent}
            onChange={(e) => setReplyContent(e.target.value)}
          />
          <button type="submit" className="submit-reply-button">Reply</button>
        </form>
      </div>
      <Footer />
    </div>
  );
}

export default PostDetail;
