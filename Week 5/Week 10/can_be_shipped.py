from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """An interface for products which need shipping."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass
