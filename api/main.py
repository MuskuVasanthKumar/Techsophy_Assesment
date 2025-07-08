from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.risk_analyzer.predictor import predict_risk_score
from services.rollback_engine.decision import should_rollback
from fastapi.middleware.cors import CORSMiddleware  

app = FastAPI(
    title="Deployment Risk Predictor API",
    description="Predicts risk and decides rollback based on deployment metrics",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DeploymentData(BaseModel):
    total_files_changed: int
    total_lines_added: int
    total_lines_deleted: int
    services_affected: int
    test_pass_rate: float
    build_time_sec: int


class RiskResponse(BaseModel):
    risk_score: float
    rollback: bool
    reason: str


@app.post("/predict-risk", response_model=RiskResponse)
def predict_risk(data: DeploymentData):
    try:
        
        commit_data = data.dict()

       
        risk_score = predict_risk_score(commit_data)

      
        rollback, reason = should_rollback(risk_score)

        return {
            "risk_score": risk_score,
            "rollback": rollback,
            "reason": reason
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
