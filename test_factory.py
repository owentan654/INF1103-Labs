import unittest

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from storage import create_product
from supplier import Supplier

SUPPLIER = Supplier("S1", "Test Supplier", "t@example.com")


class FactoryTests(unittest.TestCase):
    def test_creates_physical_product(self):
        product = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, SUPPLIER, 1.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)

    def test_creates_digital_product(self):
        product = ProductFactory.create("digital", "D1", "Editor", 49.9, 100, SUPPLIER, 250)
        self.assertIsInstance(product, DigitalProduct)

    def test_unknown_type_raises_clear_value_error(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S1", "Install", 30.0, 5, SUPPLIER)
        self.assertIn("Unknown product type: service", str(context.exception))

    def test_invalid_values_still_rejected_through_the_factory(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P1", "Lamp", -5.0, 10, SUPPLIER, 1.0)

    def test_factory_result_works_through_the_base_type(self):
        for kind in ("physical", "digital"):
            product: Product = ProductFactory.create(kind, kind[0], "X", 5.0, 1, SUPPLIER, 1.0)
            self.assertTrue(product.get_fulfilment_info())

    def test_json_round_trip_uses_the_factory(self):
        original = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, SUPPLIER, 1.5)
        rebuilt = create_product(original.to_dict(), {})
        self.assertIsInstance(rebuilt, PhysicalProduct)
        self.assertEqual(rebuilt.to_dict(), original.to_dict())


if __name__ == "__main__":
    unittest.main()