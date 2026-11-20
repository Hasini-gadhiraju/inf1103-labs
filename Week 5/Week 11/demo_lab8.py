"""Run with: python demo_lab8.py"""

from inventory import Inventory
from order import Order
from product import Product
from product_factory import ProductFactory
from supplier import Supplier


def show_product_details(product: Product) -> None:
    # Both subclasses can be passed to this function without any changes.
    product.display_information()
    print(product.get_fulfilment_info())


def main() -> None:
    supplier = Supplier("S01", "ABC Supplies", "hello@abcsupplies.com")
    physical = ProductFactory.create("physical", "P01", "Notebook", 5.00, 20, supplier, weight=0.5)
    digital = ProductFactory.create("digital", "D01", "E-book", 12.00, 30, supplier, download_size=15)

    print("=== 1. Association: Supplier and Product ===")
    physical.display_supplier()
    digital.display_supplier()
    del supplier
    print("After deleting the supplier variable:")
    physical.display_supplier()  # The product still has a reference.

    print("\n=== 2. Aggregation: Inventory and Product ===")
    inventory_a = Inventory()
    inventory_b = Inventory()
    inventory_a.add_product(physical)
    inventory_a.remove_product("P01")
    print("Still works after removal:", physical.get_name())
    inventory_b.add_product(physical)
    print("Same object in Inventory B:", inventory_b.find_product("P01") is physical)

    print("\n=== 3. Composition: Order and OrderLine ===")
    order_a = Order("O01")
    order_a.add_order_line(physical, 2)
    order_a.add_order_line(digital, 1)
    order_a.display_order()
    order_b = Order("O02")
    order_b.add_order_line(physical, 1)
    print("Different OrderLine objects:", order_a.order_lines[0] is not order_b.order_lines[0])
    print("Same Product object:", order_a.order_lines[0].product is order_b.order_lines[0].product)
    order_a.remove_order_line("D01")
    print("After removing the E-book line, total is:", f"${order_a.calculate_total():.2f}")

    print("\n=== 4. LSP and Polymorphism ===")
    inventory_b.add_product(digital)
    for product in inventory_b.products:
        show_product_details(product)
    print("Physical stock updated:", physical.update_stock(15))
    print("Digital stock updated:", digital.update_stock(25))


if __name__ == "__main__":
    main()
