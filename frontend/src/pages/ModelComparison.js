import { useEffect, useState } from "react";
import axios from "axios";
import { API_ENDPOINTS } from "../config/api";

function ModelComparison() {
  const [comparison, setComparison] = useState(null);

  useEffect(() => {
    fetchComparison();
  }, []);

  const fetchComparison = async () => {
    try {
      const res = await axios.get(API_ENDPOINTS.MODEL_COMPARISON);
      setComparison(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>ML Model Comparison</h2>
      {comparison ? (
        <div>
          {Object.keys(comparison).map((model) => (
            <div key={model} style={{ border: "1px solid gray", margin: "20px auto", padding: "20px", width: "50%" }}>
              <h3>{model}</h3>
              <p>MSE: {comparison[model].MSE}</p>
              <p>Accuracy: {comparison[model].Accuracy}%</p>
            </div>
          ))}
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default ModelComparison;
