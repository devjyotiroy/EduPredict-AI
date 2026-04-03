const mongoose = require("mongoose");

const StudentSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
  studyHours: Number,
  attendance: Number,
  previousMarks: Number,
  programmingSkill: Number,
  communicationSkill: Number,
  interestArea: String,
  mappedInterest: String,
  predictedMarks: Number,
  predictedCareer: String,
  performanceCategory: String,
  careerConfidence: Number,
  weakAreas: [String],
  recommendations: [String],
  careerRoadmap: [String],
  ensemblePrediction: mongoose.Schema.Types.Mixed,
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model("Student", StudentSchema);
