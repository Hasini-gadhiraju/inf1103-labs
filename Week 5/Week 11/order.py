from discount_strategy import DiscountStrategy, NoDiscount
from order_line import OrderLine
from product import Product


class Order:
    """Owns order lines; uses (but does not own) a discount strategy."""

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def set_discount(self, discount: DiscountStrategy) -> None:
        if not isinstance(discount, DiscountStrategy):
            raise TypeError("Discount must be a DiscountStrategy.")
        self.discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        self.order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, product_id: str) -> bool:
        for line in self.order_lines:
            if line.product.get_id() == product_id:
                self.order_lines.remove(line)
                return True
        return False

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)

    def display_order(self) -> None:
        print(f"\nOrder: {self.order_id}")
        if not self.order_lines:
            print("No order lines.")
        else:
            for line in self.order_lines:
                print(f"{line.product.get_name()} x {line.quantity} "
                      f"= ${line.calculate_subtotal():.2f}")
        print(f"Order Total: ${self.calculate_total():.2f}")

    def cancel(self) -> None:
        self.order_lines.clear()
