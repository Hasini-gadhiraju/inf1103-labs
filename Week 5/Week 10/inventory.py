from product import Product


class Inventory:
    """Keeps references to products; it does not own the products."""

    def __init__(self) -> None:
        self.products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_id()) is not None:
            return False
        self.products.append(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.products:
            if product.get_id() == product_id:
                return product
        return None

    def search_product(self, product_id: str) -> Product | None:
        # Kept from the previous lab so the menu still works.
        return self.find_product(product_id)

    def remove_product(self, product_id: str) -> bool:
        for product in self.products:
            if product.get_id() == product_id:
                self.products.remove(product)
                return True
        return False

    def display_all_products(self) -> None:
        print("\nCurrent Inventory")
        print("-" * 60)
        if not self.products:
            print("Inventory is empty.")
        else:
            for product in self.products:
                product.display_information()
        print("-" * 60)

    def display_all(self) -> None:
        self.display_all_products()

    def get_products(self) -> list[Product]:
        return self.products.copy()
