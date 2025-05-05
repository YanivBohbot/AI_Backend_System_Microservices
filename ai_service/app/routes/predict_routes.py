import datetime
from fastapi import APIRouter, Depends

from ai_service.app.model import FraudModel
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

    # log_data = {
    #     "timestamp": datetime.utcnow(),
    #     "service": "ai-service",
    #     "event": "prediction",
    #     "input": input_data.dict(),
    #     "output": {"is_fraud": bool(result_prediction)},
    #     "message": "Prediction processed successfully",
    # }

    # notify_log_service(log_data)

    # if result_prediction == 1:
    #     notify_alert_service(
    #         {
    #             "message": "Fraudulent transaction detected!",
    #             "details": FraudPredictionRequest.model_dump(),
    #         }
    #     )
    # return {"isFraud": bool(result_prediction)}
