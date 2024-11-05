import React from "react";
import { Button } from 'primereact/button';
import 'primeicons/primeicons.css';
import './Footer.css';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <h4>Connect with me on Social Media</h4>
        <div className="social-icons">
          <Button
            icon="pi pi-twitch"
            className="social-button twitch"
            onClick={() => window.open("https://www.twitch.tv/lolzayno", "_blank")}
          />
          <Button
            icon="pi pi-youtube"
            className="social-button youtube"
            onClick={() => window.open("https://www.youtube.com/@lolzayno5872", "_blank")}
          />
          <Button
            icon="pi pi-linkedin"
            className="social-button linkedin"
            onClick={() => window.open("https://www.linkedin.com/in/cameronwilliamlee/", "_blank")}
          />
          <Button
            icon="pi pi-github"
            className="social-button github"
            onClick={() => window.open("https://github.com/lolzayno", "_blank")}
          />
          <Button
            icon="pi pi-discord"
            className="social-button discord"
            onClick={() => window.open("https://discord.gg/h4p2EDzCvk", "_blank")}
          />
        </div>
        <div className="footer-links">
          <a href="/terms-of-service" target="_blank" rel="noopener noreferrer">
            Terms of Service
          </a>
          <span>|</span>
          <a href="/privacy-policy" target="_blank" rel="noopener noreferrer">
            Privacy Policy
          </a>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
