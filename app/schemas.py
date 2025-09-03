from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str

class UserOut(UserBase):
    id: int
    wallet_balance: float = Field(..., description="Current wallet balance")
    class Config:
        from_attributes = True

class WalletUpdateIn(BaseModel):
    mode: Literal["add", "set"] = Field(..., description="Use 'add' to add/subtract amount from balance, 'set' to set absolute balance")
    amount: float = Field(..., description="If mode is 'add', positive credits, negative debits. If mode is 'set', new absolute balance.")
    description: Optional[str] = None

class WalletUpdateOut(BaseModel):
    user_id: int
    new_balance: float
    transaction_id: int
    mode: str

class TxnOut(BaseModel):
    id: int
    user_id: int
    amount: float
    kind: str
    description: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True
