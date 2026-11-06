from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style contract for objects that can be shipped."""

    @abstractmethod
    def calculate_shipping_cost(self):
        pass
