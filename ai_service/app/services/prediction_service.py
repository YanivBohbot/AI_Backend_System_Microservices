import asyncio
from ai_service.app.model import FraudModel
from ai_service.app.schemas import FraudPredictionRequest, FraudPredictionResponse
from ...utils.preprocessing import preprocess_input
import httpx

# MODEL_PATH = os.path.join("model_files", "fraud_model.pkl")


class PredictionService:
    def __init__(self, model: FraudModel):
        self.model = model

    async def predict(self, data: FraudPredictionRequest) -> FraudPredictionResponse:
        features = [
            data.amount,
            self._encode_transaction_type(data.transaction_type),
            data.old_balance,
            data.new_balance,
            data.customer_age,
            self._encode_location(data.location),
        ]
        is_fraud, probability = self.model.predict(features)
        response = FraudPredictionResponse(is_fraud=is_fraud, probability=probability)

        #  run both notification and logging in parallel
        await asyncio.gather(
            self.notify_alert_service(is_fraud, probability),
            self.notify_log_service(data, is_fraud, probability),
        )
        return response

    def _encode_transaction_type(self, type_str: str) -> int:
        mapping = {"transfer": 0, "payment": 1, "withdraw": 2}
        return mapping.get(type_str.lower(), -1)

    def _encode_location(self, location: str) -> int:
        # Basic location encoding (mock)
        return sum(ord(c) for c in location) % 100

    async def notify_alert_service(self, is_fraud: bool, probability: float):
        if not is_fraud:
            return
        try:
            async with httpx.AsyncClient() as Client:
                await Client.post(
                    "http://alert-service:8003/alert",
                    json={
                        "email": "admin@example.com",
                        "message": f"🚨 Fraudulent transaction detected! is Fraud : {is_fraud}! Probability: {probability:.2f} ",
                    },
                )
        except Exception as e:
            print("Failed to notify alert service:", e)

    async def notify_log_service(
        self, data: FraudPredictionRequest, is_fraud: bool, probability: float
    ):
        try:
            async with httpx.AsyncClient() as Client:
                await Client.post(
                    "http://log-service:8004/log",
                    json={
                        "input": data.dict(),
                        "is_fraud": is_fraud,
                        "probability": probability,
                    },
                )
        except Exception as e:
            print("Failed to log prediction:", e)

