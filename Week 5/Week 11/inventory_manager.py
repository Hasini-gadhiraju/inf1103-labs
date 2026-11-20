import json
import os
from math import isfinite

from inventory import Inventory
from order import Order
from product import Product
from product_factory import ProductFactory
from discount_strategy import NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount
from input_helpers import get_positive_float
from supplier import Supplier


FILE_NAME = os.path.join(os.path.dirname(__file__), "inventory.json")


def product_from_dict(item: dict[str, object],
                      suppliers: dict[str, Supplier] | None = None) -> Product:
    """Make the right type of Product from the saved JSON data."""
    if suppliers is None:
        suppliers = {}

    saved_supplier = item.get("supplier")
    if isinstance(saved_supplier, dict):
        supplier_id = str(saved_supplier.get("id", "UNKNOWN"))
        supplier_name = str(saved_supplier.get("name", "Unknown supplier"))
        supplier_email = str(saved_supplier.get("contact_email", "Not recorded"))
    else:
        # Older lab JSON files do not have supplier details yet.
        supplier_id = "UNKNOWN"
        supplier_name = "Unknown supplier"
        supplier_email = "Not recorded"

    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier(supplier_id, supplier_name, supplier_email)
    supplier = suppliers[supplier_id]

    product_id = str(item["id"])
    name = str(item["name"])
    price = float(item["price"])
    stock = int(item["stock"])

    if not isfinite(price) or price <= 0 or stock < 0:
        raise ValueError("Price must be positive and stock non-negative.")

    product_type = item.get("type", "physical")
    return ProductFactory.create(
        str(product_type), product_id, name, price, stock, supplier,
        weight=float(item.get("weight", 0.0)),
        download_size=float(item.get("download_size", 0.0)))


def load_inventory() -> Inventory:
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}
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
                if not isinstance(item, dict):
                    raise ValueError("Product should be saved as an object.")
                product = product_from_dict(item, suppliers)
                if not inventory.add_product(product):
                    print(f"Skipping duplicate Product ID: {product.get_id()}")
            except (KeyError, TypeError, ValueError) as error:
                print(f"Skipping invalid saved product: {error}")
        print("Inventory loaded successfully.")
    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Unable to load inventory: {error}")
        print("Starting with empty inventory.")
    return inventory


def get_supplier_from_user(inventory: Inventory) -> Supplier | None:
    supplier_id = input("Supplier ID: ").strip().upper()
    if not supplier_id:
        print("Supplier ID cannot be empty.")
        return None

    # If there is already a supplier with this ID, reuse the same object.
    for product in inventory.get_products():
        if product.supplier.supplier_id == supplier_id:
            print(f"Using existing supplier: {product.supplier.name}")
            return product.supplier

    name = input("Supplier name: ").strip()
    email = input("Supplier email: ").strip()
    if not name or not email:
        print("Supplier name and email cannot be empty.")
        return None
    return Supplier(supplier_id, name, email)


def add_product(inventory: Inventory) -> None:
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
    if inventory.find_product(product_id) is not None:
        print("Product ID already exists.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return

    try:
        price = get_positive_float("Price: ")
        stock = int(input("Stock Quantity: "))
        if stock < 0:
            print("Stock cannot be negative.")
            return

        if product_type == "1":
            extra_value = float(input("Weight (kg): "))
        else:
            extra_value = float(input("Download Size (MB): "))
        if not isfinite(extra_value) or extra_value < 0:
            print("Weight or download size must not be negative.")
            return
    except ValueError:
        print("Invalid number entered.")
        return

    supplier = get_supplier_from_user(inventory)
    if supplier is None:
        return

    try:
        new_product: Product = ProductFactory.create(
            "physical" if product_type == "1" else "digital",
            product_id, name, price, stock, supplier,
            weight=extra_value if product_type == "1" else 0.0,
            download_size=extra_value if product_type == "2" else 0.0)
    except ValueError as error:
        print(f"Cannot create product: {error}")
        return

    if inventory.add_product(new_product):
        print("Product added successfully!")
    else:
        print("Product ID already exists.")


def remove_product(inventory: Inventory) -> None:
    product_id = input("Product ID to remove: ").strip().upper()
    if inventory.remove_product(product_id):
        print("Product removed from this inventory.")
    else:
        print("Product not found.")


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        return

    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    try:
        new_stock = int(input("New Stock Quantity: "))
    except ValueError:
        print("Invalid stock quantity.")
        return
    try:
        if product.update_stock(new_stock):
            print("Stock updated successfully!")
    except ValueError as error:
        print(f"Invalid stock: {error}")


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
    else:
        print("\nProduct Found")
        product.display_information()
        print("Supplier details:")
        product.display_supplier()


def save_inventory(inventory: Inventory) -> bool:
    try:
        data = [product.to_dict() for product in inventory.get_products()]
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print("Inventory saved successfully to inventory.json.")
        return True
    except OSError:
        print("Error saving inventory.")
        return False


def create_order(inventory: Inventory, orders: list[Order]) -> None:
    order_id = input("New Order ID: ").strip().upper()
    if not order_id:
        print("Order ID cannot be empty.")
        return
    for saved_order in orders:
        if saved_order.order_id == order_id:
            print("Order ID already exists.")
            return

    order = Order(order_id)
    print("Enter products for the order. Leave Product ID empty to finish.")
    while True:
        product_id = input("Product ID: ").strip().upper()
        if not product_id:
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        try:
            quantity = int(input("Quantity: "))
            order.add_order_line(product, quantity)
            print("Order line added.")
        except ValueError as error:
            print(f"Invalid quantity: {error}")

    if order.order_lines:
        orders.append(order)
        order.display_order()
        print("Orders are kept for this run; inventory data is saved separately.")
    else:
        print("No order lines entered, so the order was not saved.")


def change_order_discount(orders: list[Order]) -> None:
    """Optional menu integration showing strategies are interchangeable."""
    order_id = input("Order ID: ").strip().upper()
    order = next((order for order in orders if order.order_id == order_id), None)
    if order is None:
        print("Order not found.")
        return
    print("Discounts: 1 None | 2 Percentage | 3 Bulk | 4 Student (5%)")
    choice = input("Choose: ").strip()
    try:
        if choice == "1":
            strategy = NoDiscount()
        elif choice == "2":
            strategy = PercentageDiscount(get_positive_float("Percentage (1-100): "))
        elif choice == "3":
            strategy = BulkDiscount(get_positive_float("Threshold: "), get_positive_float("Amount: "))
        elif choice == "4":
            strategy = StudentDiscount()
        else:
            print("Invalid discount choice.")
            return
        order.set_discount(strategy)
        order.display_order()
    except ValueError as error:
        print(f"Invalid discount: {error}")


def display_orders(orders: list[Order]) -> None:
    if not orders:
        print("There are no orders yet.")
        return
    for order in orders:
        order.display_order()


def display_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Remove Product")
    print("6. Create Order")
    print("7. Display Orders")
    print("8. Save Inventory")
    print("9. Exit")
    print("10. Change Order Discount")
    print("----------------------------")


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    inventory = load_inventory()
    orders: list[Order] = []

    while True:
        display_menu()
        option = input("Enter option: ").strip()
        if option == "1":
            inventory.display_all_products()
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            remove_product(inventory)
        elif option == "6":
            create_order(inventory, orders)
        elif option == "7":
            display_orders(orders)
        elif option == "8":
            save_inventory(inventory)
        elif option == "10":
            change_order_discount(orders)
        elif option == "9":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            break
        else:
            print("Invalid option. Enter a number from 1 to 10.")


if __name__ == "__main__":
    main()
