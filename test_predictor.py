from services.risk_analyzer.predictor import predict_risk_score


sample_commit_data = {
    "total_files_changed": 10,
    "total_lines_added": 500,
    "total_lines_deleted": 300,
    "services_affected": 5,
    "test_pass_rate": 0.70,
    "build_time_sec": 400
}



risk = predict_risk_score(sample_commit_data)
print(f" Predicted Deployment Risk Score: {risk}")
    