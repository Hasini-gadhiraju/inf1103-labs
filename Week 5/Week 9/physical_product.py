from math import isfinite

from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """A Product with physical weight, fulfilling the shipping interface."""

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        weight = float(weight)
        if not isfinite(weight) or weight < 0:
            raise ValueError("Weight must be a valid non-negative number.")
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()  # Reuse the Product implementation
        print(f"  Type: Physical | Weight: {self.__weight:g} kg")
        print(f"  Fulfilment: {self.get_fulfilment_info()}")
        print(f"  Shipping cost: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self):
        return "Requires physical shipping."

    def calculate_shipping_cost(self):
        """Simple demonstration rule: $5 base fee + $2 per kilogram."""
        return 5.00 + 2.00 * self.__weight

    def to_dict(self):
        data = super().to_dict()
        data.update({"type": "physical", "weight": self.__weight})
        return data
