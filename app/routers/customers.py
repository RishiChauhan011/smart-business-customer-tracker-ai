from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Optional
from bson import ObjectId
from app.models.customer_models import Customer, CustomerCreate
from app.db.database import customer_collection
from app.dependencies import get_current_user

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(customer: CustomerCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["business", "employee"]:
        raise HTTPException(status_code=403, detail="Not authorized to add customers")

    customer_dict = customer.model_dump()
    # Business ID is the user's ID if they are a business owner
    customer_dict["business_id"] = str(current_user["_id"])
    
    result = await customer_collection.insert_one(customer_dict)
    created_customer = await customer_collection.find_one({"_id": result.inserted_id})
    created_customer["_id"] = str(created_customer["_id"])
    return created_customer

@router.get("/", response_model=List[Customer])
async def read_customers(
    search: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    current_user: dict = Depends(get_current_user)
):
    query = {"business_id": str(current_user["_id"])}
    
    # Add search logic if needed
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"email": {"$regex": search, "$options": "i"}},
        ]
        
    # Add status filter logic
    # This requires calculating pending amount on the fly
    # For simplicity, this example returns all customers
    
    customers = []
    cursor = customer_collection.find(query)
    async for customer in cursor:
        customer["_id"] = str(customer["_id"])
        customers.append(customer)
        
    return customers