import requests
import sys

BASE_URL = "http://127.0.0.1:5000/inventory"

def print_menu():
    print("\n--- INVENTORY MANAGEMENT CLI ---")
    print("1. View All Inventory")
    print("2. Add New Item Manually")
    print("3. Update Item Stock / Price")
    print("4. Delete Product")
    print("5. Fetch Product from OpenFoodFacts API")
    print("6. Exit")

def view_inventory():
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            items = response.json()
            if not items:
                print("\n[!] Inventory is currently empty.")
                return
            print(f"\n--- CURRENT INVENTORY ({len(items)} items) ---")
            for item in items:
                prod = item.get("product", {})
                print(f"ID: {item['id']} | Name: {prod.get('product_name')} | Brand: {prod.get('brands')} | Price: ${prod.get('price')} | Qty: {prod.get('quantity')}")
        else:
            print(f"\n[Error] Failed to fetch inventory. Status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("\n[Error] Could not connect to the Flask API. Make sure app.py is running!")


def add_item():
    print("\n--- Add New Item ---")
    name = input("Enter product name: ").strip()
    brand = input("Enter brand: ").strip()
    quantity = input("Enter quantity/size (e.g., 500g, 1L): ").strip()
    try:
        price = float(input("Enter price (e.g., 2.99): ").strip())
    except ValueError:
        print("[Error] Invalid price format. Must be a number.")
        return
    barcode = input("Enter barcode (optional): ").strip()

    payload = {
        "product": {
            "product_name": name,
            "brands": brand,
            "quantity": quantity,
            "price": price,
            "barcode": barcode
        }
    }

    try:
        response = requests.post(BASE_URL, json=payload)
        if response.status_code == 201:
            print("\n[Success] Item added successfully!")
        else:
            print(f"\n[Error] Failed to add item: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.ConnectionError:
        print("\n[Error] Could not connect to the Flask API.")


def update_item():
    try:
        item_id = int(input("Enter ID of the item to update: ").strip())
    except ValueError:
        print("[Error] ID must be a valid integer.")
        return

    print("\nWhat would you like to update?")
    print("1. Price")
    print("2. Quantity")
    choice = input("Select option (1 or 2): ").strip()

    payload_product = {}
    if choice == '1':
        try:
            new_price = float(input("Enter new price: ").strip())
            payload_product["price"] = new_price
        except ValueError:
            print("[Error] Invalid price.")
            return
    elif choice == '2':
        new_qty = input("Enter new quantity: ").strip()
        payload_product["quantity"] = new_qty
    else:
        print("[Error] Invalid selection.")
        return

    try:
        response = requests.patch(f"{BASE_URL}/{item_id}", json={"product": payload_product})
        if response.status_code == 200:
            print(f"\n[Success] Item {item_id} updated successfully!")
        else:
            print(f"\n[Error] {response.json().get('error', 'Failed to update')}")
    except requests.exceptions.ConnectionError:
        print("\n[Error] Could not connect to the Flask API.")