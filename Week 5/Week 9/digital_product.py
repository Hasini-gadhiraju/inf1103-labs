from math import isfinite

from product import Product


class DigitalProduct(Product):
    """A Product delivered electronically instead of being shipped."""

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        download_size = float(download_size)
        if not isfinite(download_size) or download_size < 0:
            raise ValueError("Download size must be a valid non-negative number.")
        self.__download_size = download_size

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()  # Reuse the Product implementation
        print(f"  Type: Digital | Download size: {self.__download_size:g} MB")
        print(f"  Fulfilment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self):
        return "Delivered digitally via download."

    def to_dict(self):
        data = super().to_dict()
        data.update({"type": "digital", "download_size": self.__download_size})
        return data
