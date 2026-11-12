"""Tests for Week 10 Lab 8. Run: python -m unittest discover -v"""
import contextlib
import io
import unittest
from typing import get_type_hints

from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


class TestSupplierAssociation(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S01", "ABC Supplies", "hello@abc.com")
        self.physical = PhysicalProduct("P01", "Notebook", 5.0, 20, 0.5, self.supplier)
        self.digital = DigitalProduct("D01", "E-book", 12.0, 30, 15, self.supplier)

    def test_supplier_information(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.supplier.display_information()
        self.assertIn("ABC Supplies", output.getvalue())
        self.assertIn("hello@abc.com", output.getvalue())

    def test_both_products_reference_same_supplier(self) -> None:
        self.assertIs(self.physical.supplier, self.supplier)
        self.assertIs(self.digital.supplier, self.supplier)

    def test_deleting_supplier_variable_does_not_break_products(self) -> None:
        # In this test the products are the only remaining references.
        supplier = Supplier("S02", "Another Supplier", "supplier@example.com")
        physical = PhysicalProduct("P02", "Pencil", 2, 10, 0.1, supplier)
        digital = DigitalProduct("D02", "Guide", 4, 10, 5, supplier)
        del supplier
        self.assertEqual(physical.supplier.name, "Another Supplier")
        self.assertEqual(digital.supplier.contact_email, "supplier@example.com")


class TestInventoryAggregation(unittest.TestCase):
    def setUp(self) -> None:
        supplier = Supplier("S01", "ABC Supplies", "hello@abc.com")
        self.product = PhysicalProduct("P01", "Notebook", 5, 20, 0.5, supplier)

    def test_transfer_same_product_between_inventories(self) -> None:
        a = Inventory()
        b = Inventory()
        self.assertTrue(a.add_product(self.product))
        self.assertTrue(a.remove_product("P01"))
        self.assertIsNone(a.find_product("P01"))
        self.assertEqual(self.product.get_name(), "Notebook")
        self.assertTrue(b.add_product(self.product))
        self.assertIs(b.find_product("P01"), self.product)

    def test_remove_missing_product(self) -> None:
        inventory = Inventory()
        self.assertFalse(inventory.remove_product("MISSING"))
        self.assertIsNone(inventory.find_product("MISSING"))

    def test_product_survives_inventory_being_deleted(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.product)
        del inventory
        self.assertEqual(self.product.get_id(), "P01")


class TestOrderComposition(unittest.TestCase):
    def setUp(self) -> None:
        supplier = Supplier("S01", "ABC Supplies", "hello@abc.com")
        self.physical = PhysicalProduct("P01", "Notebook", 5, 20, 0.5, supplier)
        self.digital = DigitalProduct("D01", "E-book", 12, 30, 15, supplier)

    def test_order_creates_lines_and_calculates_total(self) -> None:
        order = Order("O01")
        order.add_order_line(self.physical, 2)
        order.add_order_line(self.digital, 1)
        self.assertEqual(len(order.order_lines), 2)
        self.assertIsInstance(order.order_lines[0], OrderLine)
        self.assertEqual(order.order_lines[0].calculate_subtotal(), 10.0)
        self.assertEqual(order.calculate_total(), 22.0)

    def test_two_orders_have_different_lines_for_same_product(self) -> None:
        a = Order("O01")
        b = Order("O02")
        a.add_order_line(self.physical, 2)
        b.add_order_line(self.physical, 3)
        self.assertIsNot(a.order_lines[0], b.order_lines[0])
        self.assertIs(a.order_lines[0].product, b.order_lines[0].product)

    def test_remove_order_line_without_destroying_product(self) -> None:
        order = Order("O01")
        order.add_order_line(self.physical, 2)
        order.add_order_line(self.digital, 1)
        self.assertTrue(order.remove_order_line("D01"))
        self.assertEqual(order.calculate_total(), 10.0)
        self.assertFalse(order.remove_order_line("NOT_FOUND"))
        self.assertEqual(self.digital.get_name(), "E-book")

    def test_cancel_clears_order_lines(self) -> None:
        order = Order("O01")
        order.add_order_line(self.physical, 2)
        order.cancel()
        self.assertEqual(order.order_lines, [])
        self.assertEqual(order.calculate_total(), 0.0)
        self.assertEqual(self.physical.get_name(), "Notebook")

    def test_quantity_must_be_positive(self) -> None:
        order = Order("O01")
        with self.assertRaises(ValueError):
            order.add_order_line(self.physical, 0)
        self.assertEqual(order.order_lines, [])


class TestLSPAndPolymorphism(unittest.TestCase):
    def setUp(self) -> None:
        supplier = Supplier("S01", "ABC Supplies", "hello@abc.com")
        self.physical = PhysicalProduct("P01", "Notebook", 5, 20, 0.5, supplier)
        self.digital = DigitalProduct("D01", "E-book", 12, 30, 15, supplier)

    @staticmethod
    def show_product_details(product: Product) -> str:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            product.display_information()
            print(product.get_fulfilment_info())
        return output.getvalue()

    def test_same_function_accepts_both_subclasses(self) -> None:
        physical_output = self.show_product_details(self.physical)
        digital_output = self.show_product_details(self.digital)
        self.assertIn("physical shipping", physical_output)
        self.assertIn("digitally via download", digital_output)

    def test_one_inventory_uses_both_product_types(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.physical)
        inventory.add_product(self.digital)
        results = [item.get_fulfilment_info() for item in inventory.products]
        self.assertEqual(results, ["Requires physical shipping.",
                                   "Delivered digitally via download."])

    def test_both_subclasses_follow_update_stock_contract(self) -> None:
        for product in (self.physical, self.digital):
            with self.subTest(product=product.get_id()):
                self.assertTrue(product.update_stock(8))
                self.assertEqual(product.get_stock(), 8)
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertFalse(product.update_stock(-2))
                self.assertEqual(product.get_stock(), 8)

    def test_type_hints(self) -> None:
        self.assertIs(get_type_hints(Product.__init__)["supplier"], Supplier)
        self.assertEqual(get_type_hints(Inventory.find_product)["return"], Product | None)
        self.assertEqual(get_type_hints(Order.add_order_line)["product"], Product)
        self.assertEqual(get_type_hints(OrderLine.calculate_subtotal)["return"], float)
        self.assertEqual(get_type_hints(Inventory.__init__)["return"], type(None))


if __name__ == "__main__":
    unittest.main()
