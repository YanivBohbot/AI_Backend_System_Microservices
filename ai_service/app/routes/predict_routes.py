from fastapi import APIRouter, Depends
import httpx
from ai_service.app.model import FraudModel
from ..schemas import FraudPredictionRequest, FraudPredictionResponse
from ..services.prediction_service import PredictionService

router = APIRouter()


def get_service():
    model = FraudModel()
    return PredictionService(model)


@router.post("/predict", response_model=FraudPredictionResponse)
def predict_fraud(
    data: FraudPredictionRequest, service: PredictionService = Depends(get_service)
):
    result_prediction = service.predict(data)
    if result_prediction == 1:
        notify_alert_service(
            {
                "message": "Fraudulent transaction detected!",
                "details": FraudPredictionRequest.model_dump(),
            }
        )
    return {"isFraud": bool(result_prediction)}


def notify_alert_service(payload: dict):
    try:
        response = httpx.post("http://alert-service:8003/alert", json=payload)
        response.raise_for_status()
    except httpx.RequestError as exc:
        print(f"Error calling alert-service: {exc}")
