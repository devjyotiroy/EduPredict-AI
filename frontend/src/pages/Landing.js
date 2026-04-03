import { Link } from "react-router-dom";
import "./Landing.css";

function Landing() {
  const token = localStorage.getItem("token");

  return (
    <div className="landing">
      <section className="hero">
        <div className="hero-content">
          <h1 className="hero-title">
            Predict Your Academic Success with <span className="gradient-text">AI</span>
          </h1>
          <p className="hero-subtitle">
            Get personalized career recommendations, performance predictions, and improvement strategies powered by Machine Learning
          </p>
          {!token && (
            <div className="hero-buttons">
              <Link to="/register" className="btn btn-primary">Get Started Free</Link>
              <Link to="/about" className="btn btn-secondary">Learn More</Link>
            </div>
          )}
        </div>
        <div className="hero-image">
          <Link to={token ? "/dashboard" : "/register"} className="floating-card clickable">
            <span className="card-icon">📊</span>
            <h3>Performance Analytics</h3>
          </Link>
          <Link to={token ? "/predict" : "/register"} className="floating-card clickable delay-1">
            <span className="card-icon">🎯</span>
            <h3>Career Prediction</h3>
          </Link>
          <Link to={token ? "/history" : "/register"} className="floating-card clickable delay-2">
            <span className="card-icon">💡</span>
            <h3>Smart Recommendations</h3>
          </Link>
        </div>
      </section>

      <section className="features">
        <h2 className="section-title">Powerful Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <span className="feature-icon">🤖</span>
            <h3>AI-Powered Predictions</h3>
            <p>Advanced ML models predict your academic performance with high accuracy</p>
          </div>
          <div className="feature-card">
            <span className="feature-icon">📈</span>
            <h3>Performance Analytics</h3>
            <p>Track your progress with interactive charts and detailed insights</p>
          </div>
          <div className="feature-card">
            <span className="feature-icon">🎓</span>
            <h3>Career Guidance</h3>
            <p>Get personalized career recommendations based on your skills and interests</p>
          </div>
          <div className="feature-card">
            <span className="feature-icon">🗺️</span>
            <h3>Learning Roadmap</h3>
            <p>Receive a customized 3-year learning path for your chosen career</p>
          </div>
          <div className="feature-card">
            <span className="feature-icon">⚠️</span>
            <h3>Weak Area Detection</h3>
            <p>Identify areas that need improvement with smart analysis</p>
          </div>
          <div className="feature-card">
            <span className="feature-icon">💪</span>
            <h3>Improvement Tips</h3>
            <p>Get actionable recommendations to boost your performance</p>
          </div>
        </div>
      </section>

      <section className="stats">
        <div className="stats-grid">
          <div className="stat-card">
            <h3>95%</h3>
            <p>Prediction Accuracy</p>
          </div>
          <div className="stat-card">
            <h3>10+</h3>
            <p>ML Models</p>
          </div>
          <div className="stat-card">
            <h3>1000+</h3>
            <p>Students Helped</p>
          </div>
          <div className="stat-card">
            <h3>24/7</h3>
            <p>Available</p>
          </div>
        </div>
      </section>

      {!token && (
        <section className="cta">
          <h2>Ready to Predict Your Success?</h2>
          <p>Join thousands of students using AI to achieve their academic goals</p>
          <Link to="/register" className="btn btn-large">Start Your Journey</Link>
        </section>
      )}
    </div>
  );
}

export default Landing;
