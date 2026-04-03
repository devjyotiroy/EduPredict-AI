import { useEffect, useState } from "react";
import axios from "axios";
import { Bar, Line, Pie } from "react-chartjs-2";
import { useNavigate } from "react-router-dom";
import { API_ENDPOINTS } from "../config/api";
import "./Dashboard.css";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

function Dashboard() {
  const [analytics, setAnalytics] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get(API_ENDPOINTS.ANALYTICS, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAnalytics(res.data);
    } catch (err) {
      if (err.response?.status === 401) {
        navigate("/login");
      }
    }
  };

  if (!analytics) return <div className="loading">📊 Loading Analytics...</div>;

  const generateColors = (count) => {
    const colors = [
      "#6366f1", "#8b5cf6", "#ec4899", "#f43f5e", "#f59e0b",
      "#10b981", "#06b6d4", "#3b82f6", "#a855f7", "#ef4444"
    ];
    return Array.from({ length: count }, (_, i) => colors[i % colors.length]);
  };

  const trendData = {
    labels: analytics.performanceTrend.map((item, i) => 
      new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    ),
    datasets: [
      {
        label: "Predicted Marks",
        data: analytics.performanceTrend.map((item) => item.marks),
        borderColor: "#6366f1",
        backgroundColor: "rgba(99, 102, 241, 0.1)",
        tension: 0.4,
        fill: true,
        pointRadius: 5,
        pointHoverRadius: 7
      }
    ]
  };

  const careerLabels = Object.keys(analytics.careerDistribution);
  const careerData = {
    labels: careerLabels,
    datasets: [
      {
        label: "Career Distribution",
        data: Object.values(analytics.careerDistribution),
        backgroundColor: generateColors(careerLabels.length),
        borderWidth: 2,
        borderColor: "#fff"
      }
    ]
  };

  const weakAreasLabels = Object.keys(analytics.commonWeakAreas);
  const weakAreasData = {
    labels: weakAreasLabels,
    datasets: [
      {
        label: "Frequency",
        data: Object.values(analytics.commonWeakAreas),
        backgroundColor: generateColors(weakAreasLabels.length),
        borderRadius: 8
      }
    ]
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2>📊 Performance Analytics</h2>
        <p>Track your progress and insights</p>
      </div>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📝</div>
          <div className="stat-info">
            <h3>{analytics.totalPredictions}</h3>
            <p>Total Predictions</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">📈</div>
          <div className="stat-info">
            <h3>{analytics.averageMarks.toFixed(1)}%</h3>
            <p>Average Score</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🎯</div>
          <div className="stat-info">
            <h3>{Object.keys(analytics.careerDistribution).length}</h3>
            <p>Career Paths</p>
          </div>
        </div>
      </div>

      <div className="chart-card">
        <h3>📈 Performance Trend</h3>
        <Line data={trendData} options={{ responsive: true, maintainAspectRatio: true }} />
      </div>

      <div className="charts-row">
        <div className="chart-card half">
          <h3>🎯 Career Distribution</h3>
          <Pie data={careerData} options={{ responsive: true, maintainAspectRatio: true }} />
        </div>

        {Object.keys(analytics.commonWeakAreas).length > 0 && (
          <div className="chart-card half">
            <h3>⚠️ Common Weak Areas</h3>
            <Bar data={weakAreasData} options={{ responsive: true, maintainAspectRatio: true }} />
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;