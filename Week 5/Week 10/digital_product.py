from math import isfinite

from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A digital product delivered by download."""

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, download_size: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        download_size = float(download_size)
        if not isfinite(download_size) or download_size < 0:
            raise ValueError("Download size must be a valid non-negative number.")
        self.__download_size: float = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"  Type: Digital | Download size: {self.__download_size:g} MB")
        print(f"  Fulfilment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally via download."

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data.update({"type": "digital", "download_size": self.__download_size})
        return data
