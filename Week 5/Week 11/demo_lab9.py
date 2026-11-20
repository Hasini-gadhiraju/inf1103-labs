"""Run: python demo_lab9.py (no interactive prompts needed)."""
from csv_loader import load_products
from discount_strategy import BulkDiscount, PercentageDiscount, StudentDiscount
from inventory import Inventory
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


def main() -> None:
    supplier = Supplier("S01", "ABC Supplies", "hello@abc.com")
    physical = ProductFactory.create("physical", "P1", "Bookcase", 125, 10, supplier, weight=5)
    order = Order("O1", BulkDiscount(200, 20))
    order.add_order_line(physical, 2)
    print("Bulk total:", order.calculate_total())
    order.set_discount(PercentageDiscount(10))
    print("10% total:", order.calculate_total())
    order.set_discount(StudentDiscount())
    print("Student total:", order.calculate_total())
    inventory = Inventory()
    load_products("products.csv", inventory, supplier)
    print("Loaded product IDs:", [p.get_id() for p in inventory.get_products()])


if __name__ == "__main__":
    main()
