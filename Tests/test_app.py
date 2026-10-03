import pytest
from unittest.mock import patch
from app import app, inventory_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def reset_db():
    global inventory_db
    inventory_db.clear()
    inventory_db.extend([
        {
            "id": 1,
            "status": 1,
            "product": {
                "product_name": "Organic Almond Milk",
                "brands": "Silk",
                "ingredients_text": "Filtered water, almonds",
                "quantity": "1L",
                "price": 3.99,
                "barcode": "025293600123"
            }
        }
    ])