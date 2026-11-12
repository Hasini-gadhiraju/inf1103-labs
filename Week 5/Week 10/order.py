from order_line import OrderLine
from product import Product


class Order:
    """Creates and manages its own order lines."""

    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        # Composition: the order creates the OrderLine itself.
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for line in self.order_lines:
            if line.product.get_id() == product_id:
                self.order_lines.remove(line)
                return True
        return False

    def calculate_total(self) -> float:
        total = 0.0
        for line in self.order_lines:
            total += line.calculate_subtotal()
        return total

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
        # Clear the lines through their owning Order.
        self.order_lines.clear()
