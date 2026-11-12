from math import isfinite

from can_be_shipped import CanBeShipped
from product import Product
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """A physical product that can be shipped."""

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, weight: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        weight = float(weight)
        if not isfinite(weight) or weight < 0:
            raise ValueError("Weight must be a valid non-negative number.")
        self.__weight: float = weight

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"  Type: Physical | Weight: {self.__weight:g} kg")
        print(f"  Fulfilment: {self.get_fulfilment_info()}")
        print(f"  Shipping cost: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return 5.00 + 2.00 * self.__weight

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data.update({"type": "physical", "weight": self.__weight})
        return data
