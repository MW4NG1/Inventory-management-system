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