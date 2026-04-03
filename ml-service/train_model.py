import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
import joblib

# Load dataset
data = pd.read_csv("student_data.csv")

print("Dataset loaded:", data.shape)
print("\nCareer distribution:")
print(data["Career"].value_counts())

# Convert categorical columns to numeric
le_interest = LabelEncoder()
le_career = LabelEncoder()

data["InterestArea"] = le_interest.fit_transform(data["InterestArea"])
data["Career"] = le_career.fit_transform(data["Career"])

print("\nInterest Areas:", le_interest.classes_)
print("Careers:", le_career.classes_)

# -----------------------------
# PART 1 – PERFORMANCE MODEL (Random Forest)
# -----------------------------

X_perf = data[["StudyHours", "Attendance", "PreviousMarks",
               "ProgrammingSkill", "CommunicationSkill"]]

y_perf = data["FinalMarks"]

X_train, X_test, y_train, y_test = train_test_split(
    X_perf, y_perf, test_size=0.2, random_state=42)

# Use Random Forest instead of Linear Regression
reg_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
reg_model.fit(X_train, y_train)

pred_marks = reg_model.predict(X_test)

print("\n=== Performance Model ===")
print("R2 Score:", r2_score(y_test, pred_marks))
print("MSE:", mean_squared_error(y_test, pred_marks))

# Save performance model
joblib.dump(reg_model, "performance_model.pkl")
print("Performance model saved")

# -----------------------------
# PART 2 – CAREER MODEL (Decision Tree with better params)
# -----------------------------

X_career = data[["FinalMarks", "ProgrammingSkill",
                 "CommunicationSkill", "InterestArea"]]

y_career = data["Career"]

X_train2, X_test2, y_train2, y_test2 = train_test_split(
    X_career, y_career, test_size=0.2, random_state=42)

# Improved Decision Tree
clf = DecisionTreeClassifier(max_depth=10, min_samples_split=2, random_state=42)
clf.fit(X_train2, y_train2)

career_pred = clf.predict(X_test2)

print("\n=== Career Model ===")
print("Accuracy:", accuracy_score(y_test2, career_pred))

# Save career model
joblib.dump(clf, "career_model.pkl")
joblib.dump(le_interest, "interest_encoder.pkl")
joblib.dump(le_career, "career_encoder.pkl")

print("Career model saved")
print("Encoders saved")
print("\nTraining complete!")
