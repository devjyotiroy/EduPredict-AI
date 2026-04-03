import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./Profile.css";

function Profile() {
  const [userData, setUserData] = useState({ name: "", email: "" });
  const [profile, setProfile] = useState({
    phone: "",
    address: "",
    attendance: "",
    skills: [],
    interests: []
  });
  const [isEditing, setIsEditing] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    setUserData({ name: user.name || "", email: user.email || "" });
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get("http://localhost:5000/api/profile", {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.data._id) {
        setProfile({
          phone: res.data.phone || "",
          address: res.data.address || "",
          attendance: res.data.attendance || "",
          skills: res.data.skills || [],
          interests: res.data.interests || []
        });
      }
    } catch (err) {
      console.log(err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      await axios.post("http://localhost:5000/api/profile", profile, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert("Profile updated successfully!");
      setIsEditing(false);
    } catch (err) {
      alert("Failed to update profile");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/");
  };

  return (
    <div className="profile-page">
      <div className="profile-container">
        <div className="profile-header">
          <div className="profile-avatar">
            <span>{userData.name?.charAt(0)?.toUpperCase()}</span>
          </div>
          <h2>{userData.name}</h2>
          <p className="profile-email">{userData.email}</p>
        </div>

        <div className="profile-content">
          <div className="profile-actions">
            <button 
              onClick={() => setIsEditing(!isEditing)} 
              className="btn-edit"
            >
              {isEditing ? "Cancel" : "Edit Profile"}
            </button>
            <button onClick={handleLogout} className="btn-logout">
              Logout
            </button>
          </div>

          <form onSubmit={handleSubmit} className="profile-form">
            <div className="form-section">
              <h3>Personal Information</h3>
              
              <div className="form-group">
                <label>Name</label>
                <input
                  type="text"
                  value={userData.name}
                  disabled
                  className="input-disabled"
                />
              </div>

              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  value={userData.email}
                  disabled
                  className="input-disabled"
                />
              </div>

              <div className="form-group">
                <label>Phone</label>
                <input
                  type="tel"
                  placeholder="Enter phone number"
                  value={profile.phone}
                  onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                  disabled={!isEditing}
                />
              </div>

              <div className="form-group">
                <label>Address</label>
                <textarea
                  placeholder="Enter your address"
                  value={profile.address}
                  onChange={(e) => setProfile({ ...profile, address: e.target.value })}
                  disabled={!isEditing}
                  rows="3"
                />
              </div>
            </div>

            <div className="form-section">
              <h3>Academic Information</h3>
              
              <div className="form-group">
                <label>Attendance (%)</label>
                <input
                  type="number"
                  placeholder="Enter attendance percentage"
                  value={profile.attendance}
                  onChange={(e) => setProfile({ ...profile, attendance: e.target.value })}
                  disabled={!isEditing}
                  min="0"
                  max="100"
                />
              </div>

              <div className="form-group">
                <label>Skills (comma separated)</label>
                <input
                  type="text"
                  placeholder="e.g., Python, Java, React"
                  value={profile.skills.join(", ")}
                  onChange={(e) => setProfile({ ...profile, skills: e.target.value.split(",").map(s => s.trim()) })}
                  disabled={!isEditing}
                />
              </div>

              <div className="form-group">
                <label>Interests (comma separated)</label>
                <input
                  type="text"
                  placeholder="e.g., Web Development, AI, Data Science"
                  value={profile.interests.join(", ")}
                  onChange={(e) => setProfile({ ...profile, interests: e.target.value.split(",").map(s => s.trim()) })}
                  disabled={!isEditing}
                />
              </div>
            </div>

            {isEditing && (
              <button type="submit" className="btn-save">
                Save Changes
              </button>
            )}
          </form>
        </div>
      </div>
    </div>
  );
}

export default Profile;
