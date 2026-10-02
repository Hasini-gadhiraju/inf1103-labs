import json
import os


FILE_NAME = "inventory.json"


def load_inventory():
    if os.path.exists(FILE_NAME):
        print("inventory.json found.")

        try:
            with open(FILE_NAME, "r") as file:
                inventory = json.load(file)

            print("Inventory loaded successfully.")
            return inventory

        except json.JSONDecodeError:
            print("inventory.json is empty or invalid.")
            print("Starting with empty inventory.")
            return []

    else:
        print("inventory.json not found.")
        print("Starting with empty inventory.")
        return []


def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 60)

    if len(inventory) == 0:
        print("Inventory is empty.")

    else:
        for product in inventory:
            print(
                f"ID: {product['id']} | "
                f"Name: {product['name']} | "
                f"Price: ${product['price']:.2f} | "
                f"Stock: {product['stock']}"
            )

    print("-" * 60)


def add_product(inventory):
    print("\nAdd New Product")

    product_id = input("Product ID: ").strip().upper()

    # Check if ID already exists
    for product in inventory:
        if product["id"] == product_id:
            print("Product ID already exists.")
            return

    product_name = input("Product Name: ").strip()

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))

    except ValueError:
        print("Invalid price or stock quantity.")
        return

    if price < 0:
        print("Price cannot be negative.")
        return

    if stock < 0:
        print("Stock cannot be negative.")
        return

    new_product = {
        "id": product_id,
        "name": product_name,
        "price": price,
        "stock": stock
    }

    inventory.append(new_product)

    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")

    product_id = input("Enter Product ID: ").strip().upper()

    for product in inventory:

        if product["id"] == product_id:

            print("Product Found:")
            print(f"Name: {product['name']}")
            print(f"Current Stock: {product['stock']}")

            try:
                new_stock = int(input("New Stock Quantity: "))

            except ValueError:
                print("Invalid stock quantity.")
                return

            if new_stock < 0:
                print("Stock cannot be negative.")
                return

            product["stock"] = new_stock

            print("Stock updated successfully!")
            return

    print("Product not found.")


def search_product(inventory):
    print("\nSearch Product")

    product_id = input("Enter Product ID: ").strip().upper()

    for product in inventory:

        if product["id"] == product_id:

            print("\nProduct Found")
            print("-" * 50)
            print(f"ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']:.2f}")
            print(f"Stock: {product['stock']}")
            print("-" * 50)

            return

    print("Product not found.")


def save_inventory(inventory):
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(inventory, file, indent=4)

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
            display_all(inventory)

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