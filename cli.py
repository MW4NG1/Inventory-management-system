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