import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./History.css";

function History() {
  const [history, setHistory] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get("http://localhost:5000/api/predict/history", {
        headers: { Authorization: `Bearer ${token}` }
      });
      setHistory(res.data);
    } catch (err) {
      if (err.response?.status === 401) {
        navigate("/login");
      }
    }
  };

  const getPerformanceBadge = (category) => {
    const badges = {
      "Excellent": { emoji: "🏆", color: "#10b981" },
      "Good": { emoji: "✅", color: "#3b82f6" },
      "Average": { emoji: "⚠️", color: "#f59e0b" },
      "Needs Improvement": { emoji: "📚", color: "#ef4444" }
    };
    return badges[category] || badges["Average"];
  };

  return (
    <div className="history-container">
      <div className="history-header">
        <h2>📜 Prediction History</h2>
        <p>View all your past predictions and progress</p>
      </div>

      {history.length > 0 ? (
        <div className="history-grid">
          {history.map((item, index) => {
            const badge = getPerformanceBadge(item.performanceCategory);
            return (
              <div key={index} className="history-card">
                <div className="history-card-header">
                  <span className="history-number">#{history.length - index}</span>
                  <span className="history-date">
                    {new Date(item.createdAt).toLocaleDateString('en-US', { 
                      month: 'short', 
                      day: 'numeric', 
                      year: 'numeric' 
                    })}
                  </span>
                </div>

                <div className="history-main">
                  <div className="performance-badge" style={{ backgroundColor: badge.color }}>
                    <span className="badge-emoji">{badge.emoji}</span>
                    <span className="badge-text">{item.performanceCategory}</span>
                  </div>
                  <div className="marks-display">
                    <span className="marks-value">{item.predictedMarks}</span>
                    <span className="marks-label">Predicted Marks</span>
                  </div>
                </div>

                <div className="history-details">
                  <div className="detail-row">
                    <span className="detail-label">📚 Study Hours:</span>
                    <span className="detail-value">{item.studyHours}h</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">✅ Attendance:</span>
                    <span className="detail-value">{item.attendance}%</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">💼 Career:</span>
                    <span className="detail-value">{item.predictedCareer}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">🎯 Confidence:</span>
                    <span className="detail-value">{item.careerConfidence}%</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="no-history">
          <div className="no-history-icon">📭</div>
          <h3>No History Yet</h3>
          <p>Make your first prediction to see it here!</p>
        </div>
      )}
    </div>
  );
}

export default History;
