from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Simulated database array reflecting OpenFoodFacts structure
inventory_db = [
    {
        "id": 1,
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds, cane sugar, sea salt",
            "quantity": "1L",
            "price": 3.99,
            "barcode": "025293600123"
        }
    },
    {
        "id": 2,
        "status": 1,
        "product": {
            "product_name": "Organic Oaty Granola",
            "brands": "Nature's Path",
            "ingredients_text": "Whole grain rolled oats, cane sugar, sunflower oil",
            "quantity": "350g",
            "price": 5.49,
            "barcode": "058449650221"
        }
    }
]

# Helper function
def find_item(item_id):
    return next((item for item in inventory_db if item["id"] == item_id), None)

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory_db), 200