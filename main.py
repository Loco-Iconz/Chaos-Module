from fastapi import FastAPI
from chaos_engine import router as chaos_router

app = FastAPI(
    title="Chaos Engine API",
    version="2.0",
    description="Chaos Module backend for live game volatility and edge computation."
)

@app.get("/")
def root():
    return {"status": "ok", "message": "Chaos Module API is running"}

@app.get("/live")
def live():
    return {"status": "online", "service": "chaos-module"}

app.include_router(chaos_router)
