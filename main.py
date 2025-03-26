from fastapi import FastAPI
from api import stock, strategy
from db.connection import connect_db, disconnect_db

app = FastAPI()

# Include API routes
app.include_router(stock.router)
app.include_router(strategy.router)

@app.on_event("startup")
def startup():
    connect_db()

@app.on_event("shutdown")
def shutdown():
    disconnect_db()
