const express = require("express");
const Profile = require("../models/Profile");
const authMiddleware = require("../middleware/auth");

const router = express.Router();

// Get Profile
router.get("/", authMiddleware, async (req, res) => {
  try {
    const profile = await Profile.findOne({ userId: req.user.userId });
    res.json(profile || {});
  } catch (error) {
    console.error("Get Profile Error:", error);
    res.status(500).json({ error: error.message });
  }
});

// Update Profile
router.post("/", authMiddleware, async (req, res) => {
  try {
    const profile = await Profile.findOneAndUpdate(
      { userId: req.user.userId },
      { ...req.body, userId: req.user.userId },
      { new: true, upsert: true }
    );
    res.json(profile);
  } catch (error) {
    console.error("Update Profile Error:", error);
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
