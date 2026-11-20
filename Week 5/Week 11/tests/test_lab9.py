"""Week 11 automated tests; discover with python -m unittest discover -v."""
import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from csv_loader import load_products
from discount_strategy import (BulkDiscount, DiscountStrategy, NoDiscount,
                               PercentageDiscount, StudentDiscount)
from input_helpers import get_positive_float
from inventory import Inventory
from inventory_manager import product_from_dict
from order import Order
from order_line import OrderLine
from product_factory import ProductFactory
from supplier import Supplier


class TestWeek11(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S1", "Example", "example@test.com")
        self.product = ProductFactory.create("physical", "P1", "Chair", 125, 5,
                                             self.supplier, weight=2)

    def test_strategy_switch(self):
        order = Order("O1", BulkDiscount(200, 20))
        order.add_order_line(self.product, 2)
        self.assertEqual(order.calculate_total(), 230)
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225)
        order.set_discount(StudentDiscount())
        self.assertEqual(order.calculate_total(), 237.5)
        self.assertIsInstance(order.discount, DiscountStrategy)

    def test_default_discount_and_shared_strategy(self):
        a, b = Order("A"), Order("B")
        a.add_order_line(self.product, 1)
        self.assertIsInstance(a.discount, NoDiscount)
        self.assertEqual(a.calculate_total(), 125)
        strategy = PercentageDiscount(10)
        a.set_discount(strategy)
        b.set_discount(strategy)
        self.assertIs(a.discount, b.discount)

    def test_new_strategy_without_order_changes(self):
        class FixedDiscount(DiscountStrategy):
            def apply(self, total):
                return total - 3
        order = Order("A", FixedDiscount())
        order.add_order_line(self.product, 1)
        self.assertEqual(order.calculate_total(), 122)

    def test_factory_physical_digital_and_bad_type(self):
        digital = ProductFactory.create("digital", "D1", "Software", 20, 3,
                                        self.supplier, download_size=90)
        self.assertEqual(digital.get_download_size(), 90)
        self.assertEqual(self.product.get_weight(), 2)
        with self.assertRaisesRegex(ValueError, "Unknown product type: service"):
            ProductFactory.create("service", "S1", "Service", 5, 1, self.supplier)

    def test_validation(self):
        for price in (0, -1, float("inf"), float("nan")):
            with self.subTest(price=price), self.assertRaises(ValueError):
                ProductFactory.create("physical", "P2", "Bad", price, 1, self.supplier)
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D2", "Bad", 10, -1, self.supplier)
        with self.assertRaises(ValueError):
            self.product.update_stock(-2)
        with self.assertRaises(ValueError):
            OrderLine(self.product, 0)
        with self.assertRaises(ValueError):
            OrderLine(self.product, -2)
        self.assertEqual(self.product.get_stock(), 5)

    def test_price_input_reprompts(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            with contextlib.redirect_stdout(output):
                value = get_positive_float("Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero."])

    def test_csv_bad_rows_and_missing(self):
        inv = Inventory()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            load_products(str(Path(__file__).resolve().parent.parent / "products.csv"), inv, self.supplier)
        self.assertEqual([p.get_id() for p in inv.get_products()], ["P001", "D001", "P003"])
        self.assertIn("Skipping invalid row 4", output.getvalue())
        self.assertIn("Skipping invalid row 5", output.getvalue())
        self.assertIn("3 products loaded.", output.getvalue())
        self.assertTrue(output.getvalue().endswith("Load attempt finished.\n"))
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            with contextlib.redirect_stdout(output):
                load_products(str(Path(directory) / "missing.csv"), Inventory(), self.supplier)
        self.assertIn("Products file not found:", output.getvalue())
        self.assertIn("Load attempt finished.", output.getvalue())

    def test_json_creation_uses_factory(self):
        data = {"id": "P3", "name": "Desk", "price": 5, "stock": 2,
                "type": "physical", "weight": 1}
        self.assertEqual(product_from_dict(data).get_weight(), 1)
        data["type"] = "service"
        with self.assertRaises(ValueError):
            product_from_dict(data)


if __name__ == "__main__":
    unittest.main()
