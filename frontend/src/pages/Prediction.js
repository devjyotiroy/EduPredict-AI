import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./Prediction.css";

function Prediction() {
  const [formData, setFormData] = useState({
    studyHours: "",
    attendance: "",
    previousMarks: "",
    programmingSkill: "",
    communicationSkill: "",
    interestArea: ""
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.studyHours || formData.studyHours < 0 || formData.studyHours > 24) {
      newErrors.studyHours = "Study hours must be between 0-24";
    }
    if (!formData.attendance || formData.attendance < 0 || formData.attendance > 100) {
      newErrors.attendance = "Attendance must be between 0-100%";
    }
    if (!formData.previousMarks || formData.previousMarks < 0 || formData.previousMarks > 100) {
      newErrors.previousMarks = "Previous marks must be between 0-100";
    }
    if (formData.programmingSkill && (formData.programmingSkill < 0 || formData.programmingSkill > 3)) {
      newErrors.programmingSkill = "Programming skill must be 0, 1, 2, or 3";
    }
    if (!formData.communicationSkill || formData.communicationSkill < 1 || formData.communicationSkill > 3) {
      newErrors.communicationSkill = "Communication skill must be 1, 2, or 3";
    }
    if (!formData.interestArea || formData.interestArea.trim() === "") {
      newErrors.interestArea = "Interest area is required";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    if (errors[e.target.name]) {
      setErrors({ ...errors, [e.target.name]: "" });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      const formattedData = {
        studyHours: Number(formData.studyHours),
        attendance: Number(formData.attendance),
        previousMarks: Number(formData.previousMarks),
        programmingSkill: formData.programmingSkill ? Number(formData.programmingSkill) : 0,
        communicationSkill: Number(formData.communicationSkill),
        interestArea: formData.interestArea.trim()
      };

      const token = localStorage.getItem("token");
      const res = await axios.post(
        "http://localhost:5000/api/predict",
        formattedData,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setResult(res.data);
    } catch (error) {
      console.error(error);
      if (error.response?.status === 401) {
        alert("Session expired. Please login again.");
        navigate("/login");
      } else {
        alert("Prediction failed. Please check your input and try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="prediction-page">
      <div className="prediction-container">
        <h2 className="page-title">📊 Performance Prediction</h2>
        <p className="page-subtitle">Enter your academic details to get AI-powered predictions</p>

        <form onSubmit={handleSubmit} className="prediction-form">
          <div className="form-grid">
            <div className="form-group">
              <label>Study Hours (per day)</label>
              <input
                type="number"
                name="studyHours"
                placeholder="e.g., 5"
                value={formData.studyHours}
                onChange={handleChange}
                min="0"
                max="24"
                step="0.5"
              />
              {errors.studyHours && <span className="error">{errors.studyHours}</span>}
            </div>

            <div className="form-group">
              <label>Attendance (%)</label>
              <input
                type="number"
                name="attendance"
                placeholder="e.g., 85"
                value={formData.attendance}
                onChange={handleChange}
                min="0"
                max="100"
              />
              {errors.attendance && <span className="error">{errors.attendance}</span>}
            </div>

            <div className="form-group">
              <label>Previous Marks</label>
              <input
                type="number"
                name="previousMarks"
                placeholder="e.g., 75"
                value={formData.previousMarks}
                onChange={handleChange}
                min="0"
                max="100"
              />
              {errors.previousMarks && <span className="error">{errors.previousMarks}</span>}
            </div>

            <div className="form-group">
              <label>Programming Skill (1-3) - Optional</label>
              <select
                name="programmingSkill"
                value={formData.programmingSkill}
                onChange={handleChange}
              >
                <option value="">Select (Optional)</option>
                <option value="0">0 - None</option>
                <option value="1">1 - Beginner</option>
                <option value="2">2 - Intermediate</option>
                <option value="3">3 - Advanced</option>
              </select>
              {errors.programmingSkill && <span className="error">{errors.programmingSkill}</span>}
            </div>

            <div className="form-group">
              <label>Communication Skill (1-3)</label>
              <select
                name="communicationSkill"
                value={formData.communicationSkill}
                onChange={handleChange}
              >
                <option value="">Select</option>
                <option value="1">1 - Beginner</option>
                <option value="2">2 - Intermediate</option>
                <option value="3">3 - Advanced</option>
              </select>
              {errors.communicationSkill && <span className="error">{errors.communicationSkill}</span>}
            </div>

            <div className="form-group full-width">
              <label>Interest Area</label>
              <input
                type="text"
                name="interestArea"
                placeholder="e.g., Web Development, Data Science, AI"
                value={formData.interestArea}
                onChange={handleChange}
              />
              {errors.interestArea && <span className="error">{errors.interestArea}</span>}
            </div>
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? "Predicting..." : "🎯 Get Prediction"}
          </button>
        </form>

        {result && (
          <div className="results-section">
            <div className="result-card primary">
              <h3>📈 Predicted Marks</h3>
              <div className="result-value">{result.predictedMarks}</div>
              <div className="result-badge">{result.performanceCategory}</div>
            </div>

            <div className="result-card">
              <h3>🎓 Career Recommendation</h3>
              <div className="result-value">{result.predictedCareer}</div>
              <div className="confidence">Confidence: {result.careerConfidence}%</div>
            </div>

            {result.ensemblePrediction && (
              <div className="result-card">
                <h3>🤖 Multi-Model Predictions</h3>
                <div className="model-results">
                  <p>Ensemble: <strong>{result.ensemblePrediction.ensemble}</strong></p>
                  <p>Random Forest: {result.ensemblePrediction.randomForest}</p>
                  <p>Linear Regression: {result.ensemblePrediction.linearRegression}</p>
                  <p>Decision Tree: {result.ensemblePrediction.decisionTree}</p>
                </div>
              </div>
            )}

            {result.weakAreas && result.weakAreas.length > 0 && (
              <div className="result-card warning">
                <h3>⚠️ Weak Areas</h3>
                <ul>
                  {result.weakAreas.map((area, idx) => <li key={idx}>{area}</li>)}
                </ul>
              </div>
            )}

            {result.recommendations && result.recommendations.length > 0 && (
              <div className="result-card info">
                <h3>💡 Recommendations</h3>
                <ul>
                  {result.recommendations.map((rec, idx) => <li key={idx}>{rec}</li>)}
                </ul>
              </div>
            )}

            {result.careerRoadmap && result.careerRoadmap.length > 0 && (
              <div className="result-card success">
                <h3>🗺️ Career Roadmap</h3>
                <ul>
                  {result.careerRoadmap.map((step, idx) => <li key={idx}>{step}</li>)}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default Prediction;
