from app.model import FraudModel
from app.services.prediction_service import PredictionService


def get_prediction_service() -> PredictionService:
    model = FraudModel("app/model_files/fraud_model.pkl")
    return PredictionService(model)
