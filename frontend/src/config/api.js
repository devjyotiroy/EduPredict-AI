const API_BASE_URL = "http://localhost:5000/api";

export const API_ENDPOINTS = {
  REGISTER: `${API_BASE_URL}/auth/register`,
  LOGIN: `${API_BASE_URL}/auth/login`,
  PROFILE: `${API_BASE_URL}/profile`,
  PREDICT: `${API_BASE_URL}/predict`,
  HISTORY: `${API_BASE_URL}/predict/history`,
  ANALYTICS: `${API_BASE_URL}/predict/analytics`,
  MODEL_COMPARISON: "http://localhost:5001/model-comparison"
};

export default API_BASE_URL;
