const express = require("express");
const axios = require("axios");
const Student = require("../models/Student");
const User = require("../models/User");
const authMiddleware = require("../middleware/auth");
const { generatePredictionPDF } = require("../utils/pdfService");
const { sendPredictionReportEmail } = require("../utils/emailService");

const router = express.Router();

// Make Prediction
router.post("/", authMiddleware, async (req, res) => {
  try {
    console.log("Prediction Request:", req.body);

    const mlResponse = await axios.post(`${process.env.ML_SERVICE_URL || "http://127.0.0.1:5001"}/predict`, req.body);
    const result = mlResponse.data;

    console.log("ML Response:", result);

    const student = new Student({
      userId: req.user.userId,
      ...req.body,
      predictedMarks: result.predictedMarks,
      predictedCareer: result.predictedCareer,
      mappedInterest: result.mappedInterest,
      performanceCategory: result.performanceCategory,
      careerConfidence: result.careerConfidence,
      weakAreas: result.weakAreas,
      recommendations: result.recommendations,
      careerRoadmap: result.careerRoadmap,
      ensemblePrediction: result.ensemblePrediction
    });

    await student.save();
    console.log("Prediction saved to MongoDB");

    // Generate PDF and send email (non-blocking)
    User.findById(req.user.userId).then(async (user) => {
      if (user) {
        const pdfBuffer = await generatePredictionPDF(user.name, req.body, result);
        await sendPredictionReportEmail(user.name, user.email, pdfBuffer);
        console.log("Prediction report emailed to", user.email);
      }
    }).catch((err) => console.error("Report email error:", err.message));

    res.json(result);
  } catch (error) {
    console.error("Prediction Error:", error);
    if (error.response) {
      console.error("ML Service Error:", error.response.data);
      return res.status(500).json({ error: error.response.data.error || "ML Service Error" });
    }
    res.status(500).json({ error: error.message || "Prediction failed" });
  }
});

// Get History
router.get("/history", authMiddleware, async (req, res) => {
  try {
    const history = await Student.find({ userId: req.user.userId }).sort({ createdAt: -1 });
    res.json(history);
  } catch (error) {
    console.error("History Error:", error);
    res.status(500).json({ error: "Failed to fetch history" });
  }
});

// Get Analytics
router.get("/analytics", authMiddleware, async (req, res) => {
  try {
    const predictions = await Student.find({ userId: req.user.userId }).sort({ createdAt: 1 });
    
    const analytics = {
      totalPredictions: predictions.length,
      averageMarks: predictions.reduce((sum, p) => sum + p.predictedMarks, 0) / predictions.length || 0,
      performanceTrend: predictions.map(p => ({
        date: p.createdAt,
        marks: p.predictedMarks,
        category: p.performanceCategory
      })),
      careerDistribution: predictions.reduce((acc, p) => {
        acc[p.predictedCareer] = (acc[p.predictedCareer] || 0) + 1;
        return acc;
      }, {}),
      commonWeakAreas: predictions.flatMap(p => p.weakAreas || []).reduce((acc, area) => {
        acc[area] = (acc[area] || 0) + 1;
        return acc;
      }, {})
    };

    res.json(analytics);
  } catch (error) {
    console.error("Analytics Error:", error);
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
