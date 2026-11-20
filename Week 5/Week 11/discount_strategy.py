"""Interchangeable order discounts (Strategy pattern)."""
from abc import ABC, abstractmethod
from math import isfinite


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        """Return the total after applying the discount."""


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        if not isfinite(percentage) or not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.percentage = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        if not isfinite(threshold) or threshold < 0:
            raise ValueError("Bulk threshold must be non-negative.")
        if not isfinite(amount) or amount < 0:
            raise ValueError("Bulk discount must be non-negative.")
        self.threshold = threshold
        self.amount = amount

    def apply(self, total: float) -> float:
        return max(0.0, total - self.amount) if total >= self.threshold else total


class StudentDiscount(PercentageDiscount):
    """Extension without modifying Order: 5% off."""
    def __init__(self) -> None:
        super().__init__(5)
