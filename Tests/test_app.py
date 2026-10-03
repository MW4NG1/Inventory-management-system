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

def test_get_single_item(client):
    reset_db()
    response = client.get('/inventory/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert data['product']['product_name'] == "Organic Almond Milk"

    response_404 = client.get('/inventory/999')
    assert response_404.status_code == 404

def test_add_item(client):
    reset_db()
    payload = {
        "product": {
            "product_name": "Test Coffee",
            "brands": "Nescafe",
            "price": 5.99,
            "quantity": "200g"
        }
    }
    response = client.post('/inventory', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['product']['product_name'] == "Test Coffee"

def test_update_item(client):
    reset_db()
    payload = {
        "product": {
            "price": 4.50
        }
    }
    response = client.patch('/inventory/1', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['product']['price'] == 4.50

def test_delete_item(client):
    reset_db()
    response = client.delete('/inventory/1')
    assert response.status_code == 200
    
    # Verify deletion
    response_get = client.get('/inventory/1')
    assert response_get.status_code == 404