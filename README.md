# Python Flask Inventory Management System
A robust, modular, and fully tested RESTful Inventory Management System built with Python Flask. This application integrates seamlessly with the official OpenFoodFacts API to fetch external product data, provides an interactive Command-Line Interface (CLI) client for management, and includes a comprehensive pytest test suite.


## Project Architecture & Tech Stack
- Backend: Flask 
- External Integration: OpenFoodFacts API 
- Data Management: Local in-memory mock database array with automated ID generation
- Client Interface: Custom interactive CLI tool
- Testing Framework: Pytest with unittest.mock for mocking external network calls


## Installation and Setup Instructions
- Follow these steps to set up and run the project locally.
- Prerequisites
Python installed on your system.
pipenv installed for virtual environment and dependency management.

1. Clone the Repository
git clone https://github.com/your-username/Inventory-management-system.git
cd Inventory-management-system


2. Install Dependencies via Pipenv
pipenv install


3. Activate the Virtual Environment
pipenv shell


4. Run the Flask Server
Start the development server:
python app.py


## Project Structure
Inventory-management-system/
│
├── app.py              # Flask REST API backend
├── cli.py              # Interactive CLI frontend tool
├── Pipfile             # Pipenv dependency manager
├── Pipfile.lock        # Locked dependency versions
├── tests/
│   └── test_app.py     # pytest test suite
└── README.md           # Project documentation


## CLI Client Usage Guide
Open a second terminal window, activate your virtual environment (pipenv shell), and start the interactive CLI tool:
python cli.py


- Interactive Menu Options:
1. View All Inventory: Displays a formatted list of all items currently stored, including IDs, names, brands, prices, and quantities.
2. Add New Item Manually: Prompts you for product name, brand, size, price, and barcode to create a new manual record.
3. Update Item Stock: Allows you to enter an item ID and modify either its price or quantity dynamically.
4. Delete Product: Safely removes a product from the database array using its unique ID with confirmation prompts.
5. Fetch Product from OpenFoodFacts API: Lets you search by barcode or product name to automatically pull real-world data and save it straight to your inventory.
6. Exit: Exits the CLI program.


## Testing Instructions
- The test suite validates all CRUD routes, error handling, and mocks external API calls to prevent live network dependencies during testing.
- Run the test suite using pytest:
pipenv run python -m pytest -v


## Author
Developed as part of the Python Flask REST API and Inventory Management Lab by Mwangi Michael.






