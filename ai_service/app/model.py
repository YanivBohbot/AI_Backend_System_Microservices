import os
import joblib


class FraudModel:
    def __init__(self, model_path: str = "model_files/fraud_model.pkl"):
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            self.model = None  # fallback mock

    def predict(self, features: list) -> tuple[bool, float]:
        # Replace this with real prediction logic
        if self.model:
            prob = self.model.predict_proba([features])[0][1]
            return prob > 0.5, prob
        else:
            # Fake logic
            prob = 0.8 if features[0] > 10000 else 0.2
            return prob > 0.5, prob
