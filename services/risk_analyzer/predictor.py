
from joblib import load
import pandas as pd
from config.settings import MODEL_PATH


model = load(MODEL_PATH)

def prepare_features(commit_data):
    """
    Convert commit_data dict to a DataFrame with feature names.
    """
    return pd.DataFrame([{
        "total_files_changed": commit_data["total_files_changed"],
        "total_lines_added": commit_data["total_lines_added"],
        "total_lines_deleted": commit_data["total_lines_deleted"],
        "services_affected": commit_data["services_affected"],
        "test_pass_rate": commit_data["test_pass_rate"],
        "build_time_sec": commit_data["build_time_sec"]
    }])

def predict_risk_score(commit_data):
    features = prepare_features(commit_data)
    risk_score = model.predict_proba(features)[0][1]
    return round(risk_score, 2)
