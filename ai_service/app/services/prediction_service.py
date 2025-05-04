import pickle

from ai_service.app.model import FraudModel
from ai_service.app.schemas import FraudPredictionRequest, FraudPredictionResponse
from ...utils.preprocessing import preprocess_input


# MODEL_PATH = os.path.join("model_files", "fraud_model.pkl")


class PredictionService:
    def __init__(self, model: FraudModel):
        self.model = model

    def predict(self, data: FraudPredictionRequest) -> FraudPredictionResponse:
        features = [
            data.amount,
            self._encode_transaction_type(data.transaction_type),
            data.old_balance,
            data.new_balance,
            data.customer_age,
            self._encode_location(data.location),
        ]
        is_fraud, probability = self.model.predict(features)
        return FraudPredictionResponse(is_fraud=is_fraud, probability=probability)

    def _encode_transaction_type(self, type_str: str) -> int:
        mapping = {"transfer": 0, "payment": 1, "withdraw": 2}
        return mapping.get(type_str.lower(), -1)

    def _encode_location(self, location: str) -> int:
        # Basic location encoding (mock)
        return sum(ord(c) for c in location) % 100
