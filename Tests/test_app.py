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

def test_get_inventory(client):
    reset_db()
    response = client.get('/inventory')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1