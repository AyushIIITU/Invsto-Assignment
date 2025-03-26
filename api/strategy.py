from fastapi import APIRouter
from services.moving_average import moving_average_crossover

router = APIRouter()

@router.get("/strategy/performance")
def get_strategy_performance(short_window: int = 5, long_window: int = 20):
    return moving_average_crossover(short_window, long_window)
