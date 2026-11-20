import contextlib
import io
import unittest
from unittest.mock import patch

from input_helpers import get_positive_float
from order import Order
from orderline import OrderLine
from product_factory import ProductFactory
from supplier import Supplier

SUPPLIER = Supplier("S1", "Test Supplier", "t@example.com")


class ProductValidationTests(unittest.TestCase):
    def test_price_must_be_greater_than_zero(self):
        for bad_price in (0, -1):
            for kind in ("physical", "digital"):
                with self.assertRaises(ValueError):
                    ProductFactory.create(kind, "X", "Item", bad_price, 5, SUPPLIER, 1.0)

    def test_stock_cannot_be_negative_when_created(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "X", "Item", 10.0, -1, SUPPLIER, 1.0)

    def test_update_stock_rejects_negative_and_keeps_old_value(self):
        product = ProductFactory.create("physical", "X", "Item", 10.0, 5, SUPPLIER, 1.0)
        with self.assertRaises(ValueError):
            product.update_stock(-3)
        self.assertEqual(product.get_stock(), 5)

    def test_digital_product_enforces_the_same_stock_rule(self):
        product = ProductFactory.create("digital", "X", "Item", 10.0, 5, SUPPLIER, 1.0)
        with self.assertRaises(ValueError):
            product.update_stock(-1)


class OrderLineValidationTests(unittest.TestCase):
    def setUp(self):
        self.product = ProductFactory.create("physical", "X", "Item", 10.0, 5, SUPPLIER, 1.0)

    def test_quantity_must_be_greater_than_zero(self):
        for bad_quantity in (0, -2):
            with self.assertRaises(ValueError):
                OrderLine(self.product, bad_quantity)

    def test_valid_quantity_accepted(self):
        self.assertEqual(OrderLine(self.product, 1).get_quantity(), 1)

    def test_order_adds_no_line_when_quantity_is_invalid(self):
        order = Order("O1")
        with self.assertRaises(ValueError):
            order.add_order_line(self.product, 0)
        self.assertEqual(len(order.get_order_lines()), 0)


class InputHelperTests(unittest.TestCase):
    def test_keeps_asking_until_a_positive_number_is_entered(self):
        with patch("builtins.input", side_effect=["", "-1", "3.5"]) as fake_input, \
                contextlib.redirect_stdout(io.StringIO()):
            result = get_positive_float("Price: ")
        self.assertEqual(result, 3.5)
        self.assertEqual(fake_input.call_count, 3)


if __name__ == "__main__":
    unittest.main()