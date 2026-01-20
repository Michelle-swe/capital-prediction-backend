from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Income Prediction API",
    description="API for predicting per capita income based on year",
    version="1.0.0"
)

app.include_router(router)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
