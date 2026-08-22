from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.companies import router as companies_router
from backend.app.api.analytics import router as analytics_router


app = FastAPI(
    title="FinSight API",
    description="AI-powered financial due diligence platform",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(companies_router)
app.include_router(analytics_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to FinSight API",
        "status": "running",
    }