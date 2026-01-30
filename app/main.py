import logging
from fastapi import FastAPI, HTTPException
from app.schema import PredictInput
from app.model import predict_logic
from pathlib import Path
from typing import List
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()

MODEL_PATH = Path(__file__).resolve().parents[1] / "model" / "model.joblib"
_model = None

class PredictRequest(BaseModel):
    features: List[float] = Field(..., min_length=2)

@app.get("/health")
def health():
    return {"status":"ok", "version": "v3"}

def get_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise RuntimeError(f"model file not found: {MODEL_PATH}")
        _model = joblib.load(MODEL_PATH)
    return _model

@app.post("/predict")
def predict(req: PredictRequest):
    model = get_model()
    try:
        proba_1 = float(model.predict_proba([req.features])[0][1])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"bad input: {e}")
    pred = int(proba_1 >= 0.5)
    return {"pred": pred, "proba_1": proba_1}
