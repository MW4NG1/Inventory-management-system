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

# GET all inventory items or POST a new inventory item manually
@app.route('/inventory', methods=['GET', 'POST'])
def handle_inventory():
    if request.method == 'GET':
        return jsonify(inventory_db), 200
        
    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'product' not in data:
            return jsonify({"error": "Invalid payload, 'product' key required"}), 400
            
        prod_data = data['product']
        new_id = max([item["id"] for item in inventory_db], default=0) + 1
        
        new_entry = {
            "id": new_id,
            "status": 1,
            "product": {
                "product_name": prod_data.get('product_name', 'Unknown Product'),
                "brands": prod_data.get('brands', 'Unknown Brand'),
                "ingredients_text": prod_data.get('ingredients_text', 'Not specified'),
                "quantity": prod_data.get('quantity', 'Standard'),
                "price": float(prod_data.get('price', 0.0)),
                "barcode": prod_data.get('barcode', 'N/A')
            }
        }
        
        inventory_db.append(new_entry)
        return jsonify(new_entry), 201


@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_single_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@app.route('/inventory/fetch-external', methods=['POST'])
def fetch_external_product():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid payload"}), 400
        
    barcode = data.get('barcode')
    product_name = data.get('product_name')
    prod_info = {}
    
    if barcode:
        external_url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        response = requests.get(external_url)
        if response.status_code == 200:
            api_data = response.json()
            if api_data.get("status") == 1:
                prod_info = api_data.get("product", {})
                
    elif product_name:
        search_url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={product_name}&search_simple=1&action=process&json=1"
        response = requests.get(search_url)
        if response.status_code == 200:
            api_data = response.json()
            products = api_data.get("products", [])
            if products:
                prod_info = products[0] 
                
    if not prod_info:
        return jsonify({"error": "Product not found on OpenFoodFacts using provided barcode or name"}), 404
        
    new_id = max([item["id"] for item in inventory_db], default=0) + 1
    new_entry = {
        "id": new_id,
        "status": 1,
        "product": {
            "product_name": prod_info.get("product_name", product_name or "Unknown Product"),
            "brands": prod_info.get("brands", "Unknown Brand"),
            "ingredients_text": prod_info.get("ingredients_text", "Not specified"),
            "quantity": prod_info.get("quantity", "Standard"),
            "price": 4.99,  # Default fallback price for imported inventory
            "barcode": prod_info.get("code", barcode or "N/A")
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

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory_db
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
        
    inventory_db = [i for i in inventory_db if i["id"] != item_id]
    return jsonify({"message": f"Item {item_id} successfully deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)