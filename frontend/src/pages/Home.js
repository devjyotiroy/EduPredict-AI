import { Link, useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h1>EduPredict AI</h1>
      {token ? (
        <>
          <p>Welcome, {user.name}!</p>
          <Link to="/predict"><button>Start Prediction</button></Link>
          <Link to="/history"><button>View History</button></Link>
          <Link to="/dashboard"><button>View Analytics</button></Link>
          <Link to="/profile"><button>My Profile</button></Link>
          <Link to="/model-comparison"><button>Model Comparison</button></Link>
          <button onClick={handleLogout}>Logout</button>
        </>
      ) : (
        <>
          <Link to="/login"><button>Login</button></Link>
          <Link to="/register"><button>Register</button></Link>
        </>
      )}
    </div>
  );
}

export default Home;
