from pydantic import BaseModel


class FraudPredictionRequest(BaseModel):
    amount: float
    transaction_type: str
    old_balance: float
    new_balance: float
    customer_age: int
    location: str


class FraudPredictionResponse(BaseModel):
    is_fraud: bool
    probability: float
