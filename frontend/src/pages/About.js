import "./About.css";

function About() {
  return (
    <div className="about">
      <section className="about-hero">
        <h1>About EduPredict AI</h1>
        <p>Empowering students with AI-driven academic insights</p>
      </section>

      <section className="about-content">
        <div className="about-section">
          <h2>🎯 Our Mission</h2>
          <p>
            EduPredict AI is dedicated to helping students achieve their academic goals through 
            advanced machine learning predictions and personalized recommendations. We believe 
            every student deserves access to intelligent tools that can guide their educational journey.
          </p>
        </div>

        <div className="about-section">
          <h2>🤖 How It Works</h2>
          <div className="steps">
            <div className="step">
              <span className="step-number">1</span>
              <h3>Input Your Data</h3>
              <p>Enter your study hours, attendance, and skills</p>
            </div>
            <div className="step">
              <span className="step-number">2</span>
              <h3>AI Analysis</h3>
              <p>Our ML models analyze your data</p>
            </div>
            <div className="step">
              <span className="step-number">3</span>
              <h3>Get Predictions</h3>
              <p>Receive performance predictions and career guidance</p>
            </div>
            <div className="step">
              <span className="step-number">4</span>
              <h3>Track Progress</h3>
              <p>Monitor your improvement over time</p>
            </div>
          </div>
        </div>

        <div className="about-section">
          <h2>💡 Key Features</h2>
          <ul className="features-list">
            <li>✅ Performance Prediction using Random Forest ML</li>
            <li>✅ Career Recommendation with 87%+ accuracy</li>
            <li>✅ Weak Area Detection & Analysis</li>
            <li>✅ Personalized Improvement Recommendations</li>
            <li>✅ 3-Year Career Roadmap Generator</li>
            <li>✅ Multi-Model Ensemble Predictions</li>
            <li>✅ Interactive Analytics Dashboard</li>
            <li>✅ Complete Prediction History Tracking</li>
          </ul>
        </div>

        <div className="about-section">
          <h2>🔬 Technology Stack</h2>
          <div className="tech-grid">
            <div className="tech-card">
              <h4>Frontend</h4>
              <p>React, Chart.js</p>
            </div>
            <div className="tech-card">
              <h4>Backend</h4>
              <p>Node.js, Express</p>
            </div>
            <div className="tech-card">
              <h4>ML Service</h4>
              <p>Python, Flask, Scikit-learn</p>
            </div>
            <div className="tech-card">
              <h4>Database</h4>
              <p>MongoDB</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default About;
