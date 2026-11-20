"""CSV import using specific exceptions and try/except/else/finally."""
import csv
from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    loaded = 0
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip header
            for line_number, row in enumerate(reader, start=2):
                try:
                    if len(row) != 5:
                        raise ValueError("Expected 5 columns")
                    product_type, product_id, name, raw_price, raw_stock = row
                    product = ProductFactory.create(
                        product_type.strip(), product_id.strip(), name.strip(),
                        float(raw_price), int(raw_stock), supplier)
                    if not inventory.add_product(product):
                        raise ValueError(f"Duplicate product ID: {product_id}")
                    loaded += 1
                except ValueError as error:
                    print(f"Skipping invalid row {line_number}: {error}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
