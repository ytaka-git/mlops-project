import logging
from fastapi import FastAPI, HTTPException
from app.schema import PredictInput
from app.model import predict_logic

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/health")
def health():
    return {"status":"ok", "version": "v3"}

@app.post("/predict")
def predict(data: PredictInput):
    try:
        result = predict_logic(data.x)
        return {"result": result}
    except Exception as e:
        logger.exception("prediction failed")
        raise HTTPException(
            status_code=500,
            detail="prediction error"
        )
