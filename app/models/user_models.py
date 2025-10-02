from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class BusinessRegister(BaseModel):
    businessName: str = Field(...)
    businessEmail: EmailStr = Field(...)
    phoneNumber: str = Field(...)
    businessAddress: Optional[str] = None
    password: str = Field(...)

class User(BaseModel):
    id: str = Field(alias="_id")
    email: EmailStr
    role: str # 'business', 'employee', 'customer'
    
class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None