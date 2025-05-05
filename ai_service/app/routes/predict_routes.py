from fastapi import APIRouter, Depends

from ..model import FraudModel
from ..schemas import FraudPredictionRequest, FraudPredictionResponse
from ..services.prediction_service import PredictionService
from ..services.dependencies import get_prediction_service

router = APIRouter()

# Dependency Injection
model_instance = FraudModel()
prediction_service = PredictionService(model_instance)


@router.post("/predict", response_model=FraudPredictionResponse)
async def predict_fraud(
    input_data: FraudPredictionRequest,
    service: PredictionService = Depends(get_prediction_service),
):
    return await service.predict(input_data)
