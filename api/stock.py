from fastapi import APIRouter
from db.connection import db
from models.stocks import StockDataModel

router = APIRouter()

@router.get("/data")
def fetch_all():
    return db.stockdata.find_many()

@router.post("/data")
def insert_data(stdata: StockDataModel):
    return db.stockdata.create(data=stdata.model_dump())
