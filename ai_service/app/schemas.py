from typing import Optional
from pydantic import BaseModel


class FraudPredictionRequest(BaseModel):
    amount: float
    transaction_type: str
    old_balance: float
    new_balance: float
    customer_age: int
    ip: str
    location: Optional[str] = None


class FraudPredictionResponse(BaseModel):
    is_fraud: bool
    probability: float
