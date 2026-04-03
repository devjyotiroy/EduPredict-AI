const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:5000/api";
const ML_BASE_URL = process.env.REACT_APP_ML_URL || "http://localhost:5001";

export const API_ENDPOINTS = {
  REGISTER: `${API_BASE_URL}/auth/register`,
  LOGIN: `${API_BASE_URL}/auth/login`,
  PROFILE: `${API_BASE_URL}/profile`,
  PREDICT: `${API_BASE_URL}/predict`,
  HISTORY: `${API_BASE_URL}/predict/history`,
  ANALYTICS: `${API_BASE_URL}/predict/analytics`,
  MODEL_COMPARISON: `${ML_BASE_URL}/model-comparison`
};

export default API_BASE_URL;
