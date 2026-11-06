import json
import os
from math import isfinite

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


FILE_NAME = os.path.join(os.path.dirname(__file__), "inventory.json")


def product_from_dict(item):
    """Construct the correct subclass based on its saved type."""
    common = (item["id"], item["name"], item["price"], item["stock"])

    # Older Lab 6 files had no 'type' key. Treat those as physical
    # with unknown weight represented by 0 kg until edited/replaced.
    product_type = item.get("type", "physical")

    if product_type == "physical":
        return PhysicalProduct(*common, weight=item.get("weight", 0.0))
    if product_type == "digital":
        return DigitalProduct(*common, download_size=item["download_size"])
    raise ValueError(f"Unknown product type: {product_type}")


def load_inventory():
    inventory = Inventory()

    if not os.path.exists(FILE_NAME):
        print("inventory.json not found. Starting with empty inventory.")
        return inventory

    print("inventory.json found.")
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("Inventory must be a list of products.")

        for item in data:
            try:
                product = product_from_dict(item)
                if not inventory.add_product(product):
                    print(f"Skipping duplicate Product ID: {product.get_id()}")
            except (KeyError, TypeError, ValueError) as error:
                print(f"Skipping invalid saved product: {error}")

        print("Inventory loaded successfully.")
    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Unable to load inventory: {error}")
        print("Starting with empty inventory.")

    return inventory


def add_product(inventory):
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    product_type = input("Choose product type (1 or 2): ").strip()

    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

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

        if not isfinite(price) or price < 0:
            print("Price must be a valid non-negative number.")
            return
        if stock < 0:
            print("Stock cannot be negative.")
            return

        if product_type == "1":
            weight = float(input("Weight (kg): "))
            new_product = PhysicalProduct(product_id, product_name, price,
                                          stock, weight)
        else:
            download_size = float(input("Download Size (MB): "))
            new_product = DigitalProduct(product_id, product_name, price,
                                         stock, download_size)

    except ValueError as error:
        print(f"Invalid number or product details: {error}")
        return

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
        inventory_data = [product.to_dict()
                          for product in inventory.get_products()]
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(inventory_data, file, indent=4)
        print("Inventory saved successfully to inventory.json.")
        return True
    except OSError:
        print("Error saving inventory.")
        return False


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
