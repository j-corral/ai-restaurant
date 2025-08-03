from fastapi import FastAPI
from app.api import auth, menu, order
from app.db.session import init_db

app = FastAPI(title="Pizza Restaurant API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(menu.router, prefix="/api/menu", tags=["Menu"])
app.include_router(order.router, prefix="/api/orders", tags=["Orders"])

@app.get("/api")
def index():
    return {"hello": "world"}
