import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from joblib import dump

# Path to your Excel dataset
excel_path = "data/processed/deployment_risk_dataset.xlsx"

# Load the dataset
if not os.path.exists(excel_path):
    raise FileNotFoundError(f" Dataset not found at {excel_path}")

df = pd.read_excel(excel_path)

# Features and label
X = df[["total_files_changed", "total_lines_added", "total_lines_deleted",
        "services_affected", "test_pass_rate", "build_time_sec"]]
y = df["is_risky"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
accuracy = accuracy_score(y_test, model.predict(X_test))
print(f" Model trained with accuracy: {accuracy:.2f}")

# Save model
os.makedirs("models", exist_ok=True)
model_path = "models/risk_predictor.pkl"
dump(model, model_path)

if os.path.exists(model_path):
    print(f" Model saved successfully to: {model_path}")
else:
    print(" Model not saved.")
