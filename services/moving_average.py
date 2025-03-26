import pandas as pd
from db.connection import db, connect_db

def moving_average_crossover(short_window: int = 5, long_window: int = 20):
    try:
        connect_db()  # Ensure connection is established
        stock_data = db.stockdata.find_many()
        
        if not stock_data:
            return {"error": "No stock data available"}
        
        # Convert Prisma models to dictionaries
        stock_data_dicts = [item.model_dump() for item in stock_data]
        df = pd.DataFrame(stock_data_dicts)
        
        # Handle datetime conversion
        df["datetime"] = pd.to_datetime(df["datetime"])
        df.sort_values("datetime", inplace=True)
        
        df["short_ma"] = df["close"].rolling(window=short_window).mean()
        df["long_ma"] = df["close"].rolling(window=long_window).mean()
        
        df["signal"] = 0
        df.loc[df["short_ma"] > df["long_ma"], "signal"] = 1  # Buy
        df.loc[df["short_ma"] < df["long_ma"], "signal"] = -1  # Sell
        
        buy_signals = df[df["signal"] == 1][["datetime", "close"]].to_dict(orient="records")
        sell_signals = df[df["signal"] == -1][["datetime", "close"]].to_dict(orient="records")
        
        return {
            "short_window": short_window,
            "long_window": long_window,
            "buy_signals": buy_signals,
            "sell_signals": sell_signals,
        }
    except Exception as e:
        print(f"Error in moving_average_crossover: {e}")
        return {"error": str(e)}
    finally:
        pass
