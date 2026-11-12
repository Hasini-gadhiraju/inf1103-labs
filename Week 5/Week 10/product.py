from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """Parent class for physical and digital products."""

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        # The product knows its supplier, but does not create the supplier.
        self.supplier: Supplier = supplier

    @property
    def price(self) -> float:
        return self.__price

    def get_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_stock(self) -> int:
        return self.__stock

    def update_stock(self, quantity: int) -> bool:
        if quantity < 0:
            print("Stock cannot be negative.")
            return False
        self.__stock = quantity
        return True

    def display_supplier(self) -> None:
        self.supplier.display_information()

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | "
              f"Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | "
              f"Stock: {self.__stock}")
        print(f"  Supplier: {self.supplier.name} ({self.supplier.supplier_id})")

    def to_dict(self) -> dict[str, object]:
        # Keep supplier details when the inventory is saved as JSON.
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.supplier.to_dict(),
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Each subclass has its own way of fulfilling an order."""
        pass
