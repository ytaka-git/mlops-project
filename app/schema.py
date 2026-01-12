from pydantic import BaseModel, Field
class PredictInput(BaseModel):
    x: int = Field(..., ge=0, le=100)