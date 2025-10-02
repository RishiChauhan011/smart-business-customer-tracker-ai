from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date

class CustomerBase(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    phone: str = Field(...)
    address: Optional[str] = None
    joinedDate: date = Field(...)
    lastPayment: Optional[date] = None
    totalAmount: float = Field(default=0.0)
    paidAmount: float = Field(default=0.0)

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: str = Field(..., alias="_id")
    business_id: str
    
    @property
    def pendingAmount(self) -> float:
        return self.totalAmount - self.paidAmount