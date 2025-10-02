from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user_models import BusinessRegister, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.db.database import user_collection
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register/business", status_code=status.HTTP_201_CREATED)
async def register_business(form_data: BusinessRegister):
    # Check if user already exists
    existing_user = await user_collection.find_one({"email": form_data.businessEmail})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(form_data.password)
    
    user_data = {
        "email": form_data.businessEmail,
        "name": form_data.businessName,
        "phone": form_data.phoneNumber,
        "address": form_data.businessAddress,
        "hashed_password": hashed_password,
        "role": "business"
    }
    
    await user_collection.insert_one(user_data)
    return {"message": "Business account created successfully"}

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["email"], "role": user["role"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}