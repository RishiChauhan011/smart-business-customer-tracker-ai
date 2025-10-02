from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, customers, dashboard

app = FastAPI(
    title="BusinessTracker API",
    description="Backend for the Business Follow-up and Payment Tracker application.",
    version="1.0.0"
)

# CORS Middleware Setup
origins = [
    "http://localhost:3000", # Your React app's URL
    "http://localhost:5173", # Vite default port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(dashboard.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the BusinessTracker API!"}