
import json
import os
from product import Product
from inventory import Inventory


FILE_NAME = os.path.join(os.path.dirname(__file__), "inventory.json")


def load_inventory():
    inventory = Inventory()

    if os.path.exists(FILE_NAME):
        print("inventory.json found.")

        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)

            for item in data:
                product = Product(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"]
                )
                inventory.add_product(product)

            print("Inventory loaded successfully.")

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("inventory.json is empty or invalid.")
            print("Starting with empty inventory.")

        except OSError:
            print("Error reading inventory.json.")

    else:
        print("inventory.json not found.")
        print("Starting with empty inventory.")

    return inventory


def add_product(inventory):
    print("\nAdd New Product")

    product_id = input("Product ID: ").strip().upper()

    if not product_id:
        print("Product ID cannot be empty.")
        return

    if inventory.search_product(product_id) is not None:
        print("Product ID already exists.")
        return

    product_name = input("Product Name: ").strip()

    if not product_name:
        print("Product name cannot be empty.")
        return

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))

    except ValueError:
        print("Invalid price or stock quantity.")
        return

    if not (0 <= price < float("inf")):
        print("Price must be a valid non-negative number.")
        return

    if stock < 0:
        print("Stock cannot be negative.")
        return

    new_product = Product(product_id, product_name, price, stock)

    if inventory.add_product(new_product):
        print("Product added successfully!")
    else:
        print("Product ID already exists.")


def update_stock(inventory):
    print("\nUpdate Stock")

    product_id = input("Enter Product ID: ").strip().upper()

    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")

    try:
        new_stock = int(input("New Stock Quantity: "))

    except ValueError:
        print("Invalid stock quantity.")
        return

    if product.update_stock(new_stock):
        print("Stock updated successfully!")


def search_product(inventory):
    print("\nSearch Product")

    product_id = input("Enter Product ID: ").strip().upper()

    product = inventory.search_product(product_id)

    if product is not None:
        print("\nProduct Found")
        print("-" * 50)
        product.display_information()
        print("-" * 50)
    else:
        print("Product not found.")


def save_inventory(inventory):
    try:
        inventory_data = [
            product.to_dict()
            for product in inventory.get_products()
        ]

        with open(FILE_NAME, "w") as file:
            json.dump(inventory_data, file, indent=4)

        print("Inventory saved successfully to inventory.json.")

    except OSError:
        print("Error saving inventory.")


def display_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():

    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()

    while True:

        display_menu()
        option = input("Enter option: ").strip()

        if option == "1":
            inventory.display_all()

        elif option == "2":
            add_product(inventory)

        elif option == "3":
            update_stock(inventory)

        elif option == "4":
            search_product(inventory)

        elif option == "5":
            print("Saving inventory...")
            save_inventory(inventory)

        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)

            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("Invalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
