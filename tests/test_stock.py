import unittest
import os
from fastapi.testclient import TestClient
from main import app
import pandas as pd
from db.connection import connect_db, disconnect_db

client = TestClient(app)

def load_test_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "test_stock.csv")
    return pd.read_csv(csv_path)

class TestStockAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        connect_db()
        cls.df = load_test_data()
    
    @classmethod
    def tearDownClass(cls):
        disconnect_db()
    
    def test_insert_valid_data(self):
        invalid_data = {
            "datetime": "invalid_date",
            "open": "invalid",
            "high": "invalid",
            "low": "invalid",
            "close": "invalid",
            "volume": "invalid"
        }
        
        response = client.post("/data", json=invalid_data)
        self.assertNotEqual(response.status_code, 200) 

    def test_insert_invalid_data(self):
        invalid_data = {
            "datetime": "invalid_date",
            "open": "invalid",
            "high": "invalid",
            "low": "invalid",
            "close": "invalid",
            "volume": "invalid"
        }
        response = client.post("/data", json=invalid_data) 
        self.assertNotEqual(response.status_code, 200)
        
    def test_moving_average_crossover(self):
        response = client.get("/strategy/performance?short_window=5&long_window=20")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("buy_signals", data)
        self.assertIn("sell_signals", data)

if __name__ == "__main__":
    unittest.main()