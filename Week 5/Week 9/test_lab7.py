"""Run: python -m unittest -v test_lab7.py"""
import contextlib
import io
import json
import os
import tempfile
import unittest
from unittest.mock import patch

import inventory_manager
from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct
from product import Product


class TestProductClasses(unittest.TestCase):
    def test_physical_inheritance_and_shipping(self):
        physical = PhysicalProduct("P1", "Book", 20.0, 3, 1.5)
        self.assertIsInstance(physical, Product)
        self.assertIsInstance(physical, CanBeShipped)
        self.assertEqual(physical.get_weight(), 1.5)
        self.assertEqual(physical.calculate_shipping_cost(), 8.0)
        self.assertIn("physical shipping", physical.get_fulfilment_info())
        self.assertEqual(physical.to_dict()["type"], "physical")

    def test_different_weights_change_shipping_cost(self):
        light = PhysicalProduct("P1", "Pen", 1.0, 5, 0.5)
        heavy = PhysicalProduct("P2", "Box", 10.0, 4, 4.0)
        self.assertEqual(light.calculate_shipping_cost(), 6.0)
        self.assertEqual(heavy.calculate_shipping_cost(), 13.0)

    def test_digital_inheritance_and_fulfilment(self):
        digital = DigitalProduct("D1", "E-book", 8.5, 10, 120)
        self.assertIsInstance(digital, Product)
        self.assertNotIsInstance(digital, CanBeShipped)
        self.assertFalse(hasattr(digital, "calculate_shipping_cost"))
        self.assertEqual(digital.get_download_size(), 120.0)
        self.assertIn("digitally", digital.get_fulfilment_info())
        self.assertEqual(digital.to_dict()["type"], "digital")

    def test_method_overriding_includes_parent_information(self):
        for item, expected in (
            (PhysicalProduct("P1", "Chair", 44.0, 2, 3), "Weight: 3 kg"),
            (DigitalProduct("D1", "Music", 7.0, 5, 80), "Download size: 80 MB"),
        ):
            with self.subTest(item=item.get_id()):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    item.display_information()
                self.assertIn(f"ID: {item.get_id()}", output.getvalue())
                self.assertIn("Price: $", output.getvalue())
                self.assertIn(expected, output.getvalue())

    def test_abstract_product_and_interface_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Product("G1", "Generic", 1.0, 1)
        with self.assertRaises(TypeError):
            CanBeShipped()

    def test_invalid_specialised_values(self):
        with self.assertRaises(ValueError):
            PhysicalProduct("P", "Bad", 1, 1, -2)
        with self.assertRaises(ValueError):
            DigitalProduct("D", "Bad", 1, 1, float("inf"))


class TestInventory(unittest.TestCase):
    def test_operations_with_both_types(self):
        inventory = Inventory()
        physical = PhysicalProduct("P1", "Phone", 200, 5, 0.2)
        digital = DigitalProduct("D1", "App", 10, 99, 40)
        self.assertTrue(inventory.add_product(physical))
        self.assertTrue(inventory.add_product(digital))
        self.assertFalse(inventory.add_product(physical))
        self.assertIs(inventory.search_product("D1"), digital)
        self.assertIsNone(inventory.search_product("missing"))
        self.assertTrue(digital.update_stock(70))
        self.assertFalse(digital.update_stock(-1))
        self.assertEqual(digital.get_stock(), 70)
        self.assertEqual(len(inventory.get_products()), 2)

    def test_json_save_and_reload_preserves_types_and_values(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "inventory.json")
            inventory = Inventory()
            inventory.add_product(PhysicalProduct("P1", "Keyboard", 30, 4, 0.9))
            inventory.add_product(DigitalProduct("D1", "Software", 50, 8, 250))

            with patch.object(inventory_manager, "FILE_NAME", path):
                self.assertTrue(inventory_manager.save_inventory(inventory))
                with open(path, encoding="utf-8") as file:
                    raw = json.load(file)
                self.assertEqual({x["type"] for x in raw}, {"physical", "digital"})
                loaded = inventory_manager.load_inventory()

            p = loaded.search_product("P1")
            d = loaded.search_product("D1")
            self.assertIsInstance(p, PhysicalProduct)
            self.assertIsInstance(d, DigitalProduct)
            self.assertEqual(p.get_weight(), 0.9)
            self.assertEqual(d.get_download_size(), 250)
            self.assertEqual(d.get_stock(), 8)

    def test_old_lab6_json_still_loads(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "inventory.json")
            with open(path, "w", encoding="utf-8") as file:
                json.dump([{"id": "10", "name": "j", "price": 10.0,
                            "stock": 10}], file)
            with patch.object(inventory_manager, "FILE_NAME", path):
                loaded = inventory_manager.load_inventory()
            item = loaded.search_product("10")
            self.assertIsInstance(item, PhysicalProduct)
            self.assertEqual(item.get_weight(), 0.0)


if __name__ == "__main__":
    unittest.main()
