import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/");
  };

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          <span className="logo-icon">🎓</span>
          EduPredict AI
        </Link>

        <div className="nav-menu">
          {token ? (
            <>
              <Link to="/" className="nav-link" data-icon="🏠">Home</Link>
              <Link to="/about" className="nav-link" data-icon="ℹ️">About</Link>
              <Link to="/predict" className="nav-link" data-icon="🎯">Predict</Link>
              <Link to="/dashboard" className="nav-link" data-icon="📊">Analytics</Link>
              <Link to="/history" className="nav-link" data-icon="📜">History</Link>
              <Link to="/profile" className="nav-link profile-link" data-icon="👤">
                <span className="profile-icon">👤</span>
                <span>{user.name?.split(' ')[0]}</span>
              </Link>
            </>
          ) : (
            <>
              <Link to="/" className="nav-link" data-icon="🏠">Home</Link>
              <Link to="/about" className="nav-link" data-icon="ℹ️">About</Link>
              <Link to="/login" className="nav-link" data-icon="🔐">Login</Link>
              <Link to="/register" className="nav-btn">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
