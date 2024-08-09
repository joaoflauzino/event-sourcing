from pydantic import BaseModel


# Pydantic models for request validation
class Operation(BaseModel):
    account_id: int
    amount: float
