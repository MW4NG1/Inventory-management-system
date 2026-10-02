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


@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_single_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@app.route('/inventory', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or 'product' not in data:
        return jsonify({"error": "Invalid payload, 'product' data required"}), 400
    
    new_id = max([item["id"] for item in inventory_db], default=0) + 1
    new_entry = {
        "id": new_id,
        "status": 1,
        "product": {
            "product_name": data['product'].get('product_name', 'Unknown'),
            "brands": data['product'].get('brands', 'Unknown'),
            "ingredients_text": data['product'].get('ingredients_text', ''),
            "quantity": data['product'].get('quantity', '1 unit'),
            "price": float(data['product'].get('price', 0.0)),
            "barcode": data['product'].get('barcode', '')
        }
    }
    
    inventory_db.append(new_entry)
    return jsonify(new_entry), 201


@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
        
    data = request.get_json()
    if not data or 'product' not in data:
        return jsonify({"error": "Invalid payload"}), 400
        
    prod_data = data['product']
    for key, value in prod_data.items():
        if key in item["product"]:
            item["product"][key] = value
            
    return jsonify(item), 200