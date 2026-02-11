from fastapi import FastAPI
from chaos_engine import router as chaos_router

app = FastAPI(
    title="Chaos Engine API",
    version="2.0",
    description="Production-ready Chaos Engine backend."
)

# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------
@app.get("/")
def root():
    return {"status": "online", "service": "chaos-module"}

# ---------------------------------------------------------
# Mount Chaos Engine Router
# ---------------------------------------------------------
app.include_router(chaos_router)

