
class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.search_product(product.get_id()) is not None:
            return False

        self.__products.append(product)
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_id() == product_id:
                return product

        return None

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 60)

        if len(self.__products) == 0:
            print("Inventory is empty.")
        else:
            for product in self.__products:
                product.display_information()

        print("-" * 60)

    def get_products(self):
        return self.__products.copy()
