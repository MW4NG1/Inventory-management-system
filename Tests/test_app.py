import pytest
from unittest.mock import patch
from app import app, inventory_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client