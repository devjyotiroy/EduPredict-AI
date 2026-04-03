# EduPredict AI - Student Performance & Career Prediction System

> A comprehensive AI-powered platform for predicting student performance and career paths with personalized recommendations.

## 🌟 Overview

EduPredict AI is a full-stack machine learning application that helps students predict their academic performance and discover suitable career paths based on their study habits, skills, and interests. The system provides personalized recommendations and tracks progress over time.

## ✨ Key Features

### 🔐 Authentication & Security
- JWT-based secure authentication
- Password encryption with bcrypt
- Protected routes and session management
- 7-day token expiration

### 👤 Profile Management
- Personal information storage
- Academic history tracking
- Skills and interests management
- Editable profile with real-time updates

### 🎯 Smart Predictions
- **Performance Prediction**: ML-powered marks prediction (0-100)
- **Career Recommendation**: AI-based career path suggestions
- **Confidence Score**: Career match confidence percentage
- **Performance Category**: Excellent/Good/Average/Needs Improvement

### 📊 Analytics Dashboard
- Performance trend visualization (Line charts)
- Career distribution analysis (Pie charts)
- Weak areas identification (Bar charts)
- Progress tracking over time
- Summary statistics

### 🎓 Personalized Insights
- Automatic weak area detection
- Customized improvement recommendations
- Career roadmap generation
- Study hour suggestions
- Skill development tips

### 📜 History & Tracking
- Complete prediction history
- Date-wise tracking
- Performance trends
- Progress monitoring

### 🤖 ML Model Comparison
- Compare multiple ML algorithms
- Accuracy metrics (MSE, R²)
- Model performance visualization
- Ensemble predictions

## 🏗️ System Architecture

```
┌─────────────────┐
│   Frontend      │  React + Chart.js
│   Port: 3000    │  Modern UI/UX
└────────┬────────┘
         │ HTTP/JWT
         │
┌────────▼────────┐
│   Backend       │  Node.js + Express
│   Port: 5000    │  REST API
└────────┬────────┘
         │
         ├──────────────┐
         │              │
┌────────▼────────┐ ┌──▼──────────┐
│   MongoDB       │ │ ML Service  │  Flask + Scikit-learn
│   Database      │ │ Port: 5001  │  AI Models
└─────────────────┘ └─────────────┘
```

## 📁 Project Structure

```
EduPredict-AI/
├── backend/
│   ├── models/
│   │   ├── User.js          # User authentication
│   │   ├── Profile.js       # Student profiles
│   │   └── Student.js       # Prediction records
│   ├── routes/
│   │   ├── auth.js          # Auth endpoints
│   │   ├── profile.js       # Profile endpoints
│   │   └── prediction.js    # Prediction endpoints
│   ├── middleware/
│   │   └── auth.js          # JWT middleware
│   ├── server.js            # Express server
│   ├── .env                 # Environment variables
│   └── package.json
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Landing.js         # Home page
│   │   │   ├── About.js           # About page
│   │   │   ├── Login.js           # Login page
│   │   │   ├── Register.js        # Registration
│   │   │   ├── Profile.js         # Profile management
│   │   │   ├── Prediction.js      # Prediction form
│   │   │   ├── History.js         # History view
│   │   │   ├── Dashboard.js       # Analytics
│   │   │   └── ModelComparison.js # Model comparison
│   │   ├── components/
│   │   │   ├── Navbar.js          # Navigation
│   │   │   └── Footer.js          # Footer
│   │   └── App.js
│   └── package.json
└── ml-service/
    ├── app.py                     # Flask ML API
    ├── train_model.py             # Model training
    ├── performance_model.pkl      # Trained model
    ├── career_model.pkl           # Career model
    ├── interest_encoder.pkl       # Interest encoder
    ├── career_encoder.pkl         # Career encoder
    └── student_data.csv           # Training data
```

## 🚀 Quick Start

### Prerequisites
- Node.js (v14+)
- Python (v3.8+)
- MongoDB (local or Atlas)

### 1️⃣ Backend Setup

```bash
cd backend
npm install
```

Create `.env` file:
```env
MONGO_URI=mongodb://localhost:27017/edupredict
JWT_SECRET=your_super_secret_jwt_key_change_in_production
PORT=5000
```

Start server:
```bash
npm start
```
✅ Backend running on http://localhost:5000

### 2️⃣ ML Service Setup

```bash
cd ml-service
pip install flask joblib numpy pandas scikit-learn flask-cors
```

Train models (first time only):
```bash
python train_model.py
```

Start ML service:
```bash
python app.py
```
✅ ML Service running on http://localhost:5001

### 3️⃣ Frontend Setup

```bash
cd frontend
npm install
npm start
```
✅ Frontend running on http://localhost:3000

## 🔌 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securePassword123"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securePassword123"
}
```

### Profile Endpoints (Protected)

#### Get Profile
```http
GET /api/profile
Authorization: Bearer <token>
```

#### Update Profile
```http
POST /api/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "phone": "1234567890",
  "address": "123 Main St",
  "attendance": 85,
  "skills": ["JavaScript", "Python"],
  "interests": ["Web Development"]
}
```

### Prediction Endpoints (Protected)

#### Make Prediction
```http
POST /api/predict
Authorization: Bearer <token>
Content-Type: application/json

{
  "studyHours": 5,
  "attendance": 85,
  "previousMarks": 75,
  "programmingSkill": 2,
  "communicationSkill": 2,
  "interestArea": "Web Development"
}
```

#### Get History
```http
GET /api/predict/history
Authorization: Bearer <token>
```

#### Get Analytics
```http
GET /api/predict/analytics
Authorization: Bearer <token>
```

### ML Service Endpoints

#### Predict
```http
POST http://localhost:5001/predict
Content-Type: application/json

{
  "studyHours": 5,
  "attendance": 85,
  "previousMarks": 75,
  "programmingSkill": 2,
  "communicationSkill": 2,
  "interestArea": "Web Development"
}
```

#### Model Comparison
```http
GET http://localhost:5001/model-comparison
```

## 🤖 Machine Learning Models

### Performance Prediction
- **Algorithm**: Random Forest Regressor
- **Features**: Study Hours, Attendance, Previous Marks, Programming Skill, Communication Skill
- **Output**: Predicted Marks (0-100)

### Career Prediction
- **Algorithm**: Decision Tree Classifier
- **Features**: Predicted Marks, Skills, Interest Area
- **Output**: Career Path + Confidence Score

### Ensemble Prediction
- Combines Random Forest, Linear Regression, and Decision Tree
- Provides average prediction for better accuracy

### Supported Career Paths
- Software Engineer, Web Developer, Android Developer
- Data Scientist, AI Engineer, ML Engineer
- UI/UX Designer, Graphic Designer, Video Editor
- Business Analyst, Digital Marketer, Product Manager
- And 50+ more careers across all fields

## 🎯 Usage Guide

### Step 1: Register/Login
1. Open http://localhost:3000
2. Click "Register" to create account
3. Login with credentials

### Step 2: Update Profile
1. Navigate to Profile page
2. Click "Edit Profile"
3. Add personal and academic details
4. Save changes

### Step 3: Make Prediction
1. Go to Prediction page
2. Fill in the form:
   - Study Hours (0-24)
   - Attendance % (0-100)
   - Previous Marks (0-100)
   - Programming Skill (0-3)
   - Communication Skill (1-3)
   - Interest Area (any field)
3. Click "Get Prediction"

### Step 4: View Results
- Predicted Marks
- Performance Category
- Career Recommendation
- Confidence Score
- Weak Areas
- Improvement Recommendations
- Career Roadmap
- Ensemble Predictions

### Step 5: Track Progress
- View History page for all predictions
- Check Dashboard for analytics
- Monitor performance trends

## 🛡️ Security Features

- **Password Hashing**: bcrypt with 10 salt rounds
- **JWT Tokens**: Secure token-based authentication
- **Protected Routes**: Middleware validation
- **User Isolation**: Each user sees only their data
- **Token Expiration**: 7-day automatic expiry
- **CORS Protection**: Configured for security

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Instagram-style Navigation**: Bottom nav on mobile
- **Modern Cards**: Clean card-based layouts
- **Smooth Animations**: Engaging user experience
- **Color-coded Performance**: Visual feedback
- **Interactive Charts**: Chart.js visualizations
- **Loading States**: User feedback during operations

## 📊 Analytics Features

### Dashboard Includes:
- **Total Predictions**: Count of all predictions
- **Average Score**: Overall performance average
- **Career Paths**: Number of different careers explored
- **Performance Trend**: Line chart showing progress
- **Career Distribution**: Pie chart of career interests
- **Weak Areas**: Bar chart of common weaknesses

## 🔧 Technologies Used

### Frontend
- React 18
- React Router v6
- Axios
- Chart.js
- CSS3 (Custom styling)

### Backend
- Node.js
- Express.js
- MongoDB + Mongoose
- JWT (jsonwebtoken)
- Bcrypt.js
- CORS

### ML Service
- Python 3.8+
- Flask
- Scikit-learn
- Pandas
- NumPy
- Joblib

### Database
- MongoDB (Local or Atlas)

## 📝 Environment Variables

### Backend (.env)
```env
MONGO_URI=mongodb://localhost:27017/edupredict
JWT_SECRET=your_secret_key_here
PORT=5000
```

### ML Service (optional .env)
```env
FLASK_ENV=development
FLASK_PORT=5001
```

## 🐛 Troubleshooting

### Backend won't start
- Check MongoDB is running
- Verify .env file exists
- Check port 5000 is available

### ML Service errors
- Ensure Python packages installed
- Run `python train_model.py` first
- Check .pkl files exist

### Frontend issues
- Clear browser cache
- Check backend/ML service running
- Verify API endpoints in code

### CORS errors
- Check CORS configuration in backend
- Verify ML service has flask-cors installed

## 🚀 Deployment

### Backend (Heroku/Railway)
1. Set environment variables
2. Use MongoDB Atlas for database
3. Deploy with `git push`

### Frontend (Vercel/Netlify)
1. Update API URLs to production
2. Build: `npm run build`
3. Deploy build folder

### ML Service (Render/Railway)
1. Add requirements.txt
2. Set Python version
3. Deploy with Flask

## 📄 License

This project is created for educational purposes.

## 👥 Contributors

Developed as a final year project for student performance prediction and career guidance.

## 📞 Support

For issues or questions, please create an issue in the repository.

---

**Made with ❤️ for students by students**
