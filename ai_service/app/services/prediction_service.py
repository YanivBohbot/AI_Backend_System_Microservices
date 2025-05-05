import asyncio
from datetime import datetime
import httpx
from ..model import FraudModel
from ..schemas import FraudPredictionRequest, FraudPredictionResponse
import logging

logger = logging.getLogger("log-service")
logging.basicConfig(level=logging.INFO)


# MODEL_PATH = os.path.join("model_files", "fraud_model.pkl")


class PredictionService:
    def __init__(self, model: FraudModel):
        self.model = model

    async def predict(self, data: FraudPredictionRequest) -> FraudPredictionResponse:
        location = data.location

        if data.ip:
            try:
                async with httpx.AsyncClient() as Client:
                    response = await Client.get(
                        f"http://localhost:8005/geoip/{data.ip}"
                    )
                    response.raise_for_status()
                    geo_data = response.json()
                    logger.info(f"{geo_data}")
                    location = geo_data.get("city") or location
            except Exception as e:
                print("[WARNING] GeoIP fetch failed:", e)

            features = [
                data.amount,
                self._encode_transaction_type(data.transaction_type),
                data.old_balance,
                data.new_balance,
                data.customer_age,
                self._encode_location(location),
            ]
            is_fraud, probability = self.model.predict(features)
            response = FraudPredictionResponse(
                is_fraud=is_fraud, probability=probability
            )

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
        # if not is_fraud:
        #     return
        try:
            async with httpx.AsyncClient() as Client:
                await Client.post(
                    "http://localhost:8003/alert/",
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
            log_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "service": "ai-service",
                "event": "prediction",
                "input": data.dict(),
                "output": {"is_fraud": is_fraud, "probability": probability},
                "message": f"Prediction processed successfully with {probability:.2f} probability",
            }
            async with httpx.AsyncClient() as Client:
                await Client.post(
                    "http://localhost:8004/logs/",
                    json=log_data,
                )
        except Exception as e:
            print("Failed to log prediction:", e)
