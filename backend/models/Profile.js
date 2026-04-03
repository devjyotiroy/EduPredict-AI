const mongoose = require("mongoose");

const ProfileSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
  academicHistory: [{
    year: String,
    grade: String,
    percentage: Number
  }],
  skills: [String],
  interests: [String],
  attendance: Number,
  phone: String,
  address: String,
  updatedAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model("Profile", ProfileSchema);
