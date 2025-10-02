from fastapi import APIRouter, Depends, HTTPException
from app.db.database import customer_collection
from app.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/business")
async def get_business_dashboard_stats(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != 'business':
        raise HTTPException(status_code=403, detail="Access forbidden")

    business_id = str(current_user["_id"])
    
    # Aggregation pipeline to calculate stats
    pipeline = [
        {"$match": {"business_id": business_id}},
        {"$group": {
            "_id": "$business_id",
            "total_customers": {"$sum": 1},
            "total_paid": {"$sum": "$paidAmount"},
            "total_revenue": {"$sum": "$totalAmount"}
        }},
        {"$project": {
            "_id": 0,
            "total_customers": 1,
            "total_paid": 1,
            "pending_payments": {"$subtract": ["$total_revenue", "$total_paid"]}
        }}
    ]

    stats_cursor = customer_collection.aggregate(pipeline)
    stats = await stats_cursor.to_list(length=1)
    
    if not stats:
        return {
            "total_customers": 0,
            "total_paid": 0,
            "pending_payments": 0
        }

    return stats[0]