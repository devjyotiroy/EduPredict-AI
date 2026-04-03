import "./Footer.css";

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section">
          <h3>🎓 EduPredict AI</h3>
          <p>Predicting your academic success with AI-powered insights</p>
        </div>
        
        <div className="footer-section">
          <h4>Quick Links</h4>
          <a href="/">Home</a>
          <a href="/about">About</a>
          <a href="/login">Login</a>
        </div>
        
        <div className="footer-section">
          <h4>Features</h4>
          <a href="/predict">Performance Prediction</a>
          <a href="/dashboard">Analytics Dashboard</a>
          <a href="/model-comparison">Model Comparison</a>
        </div>
        
        <div className="footer-section">
          <h4>Contact</h4>
          <p>📧 info@edupredict.ai</p>
          <p>📱 +91 1234567890</p>
        </div>
      </div>
      
      <div className="footer-bottom">
        <p>&copy; 2024 EduPredict AI. All rights reserved.</p>
      </div>
    </footer>
  );
}

export default Footer;
