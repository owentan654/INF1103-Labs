import ast
import inspect
import textwrap
import unittest

from discount_strategy import (DiscountStrategy, NoDiscount, PercentageDiscount,
                               BulkDiscount, StudentDiscount)
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


def make_order(discount: DiscountStrategy | None = None) -> Order:
    """An order whose lines add up to 300 (3 x 100)."""
    supplier = Supplier("S1", "Test Supplier", "t@example.com")
    product = ProductFactory.create("physical", "T1", "Item", 100.0, 50, supplier, 1.0)
    order = Order("O1", discount)
    order.add_order_line(product, 3)
    return order


class StrategyTests(unittest.TestCase):
    def test_strategy_base_class_is_abstract(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()

    def test_no_discount_returns_total_unchanged(self):
        self.assertAlmostEqual(NoDiscount().apply(300), 300)

    def test_percentage_discount(self):
        self.assertAlmostEqual(PercentageDiscount(20).apply(300), 240)

    def test_bulk_discount_below_and_at_threshold(self):
        self.assertAlmostEqual(BulkDiscount(500, 50).apply(300), 300)
        self.assertAlmostEqual(BulkDiscount(300, 50).apply(300), 250)

    def test_student_discount(self):
        self.assertAlmostEqual(StudentDiscount().apply(200), 190)

    def test_invalid_percentage_rejected(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(150)


class OrderUsesStrategyTests(unittest.TestCase):
    def test_order_defaults_to_no_discount(self):
        self.assertAlmostEqual(make_order().calculate_total(), 300)

    def test_order_calculates_total_through_strategy(self):
        self.assertAlmostEqual(make_order(PercentageDiscount(20)).calculate_total(), 240)

    def test_set_discount_changes_strategy_on_existing_order(self):
        order = make_order(BulkDiscount(100, 30))
        self.assertAlmostEqual(order.calculate_total(), 270)
        order.set_discount(PercentageDiscount(50))
        self.assertAlmostEqual(order.calculate_total(), 150)

    def test_new_strategy_works_without_changing_order(self):
        class FlatTenOff(DiscountStrategy):          # a brand-new strategy, defined here
            def apply(self, total: float) -> float:
                return total - 10
        self.assertAlmostEqual(make_order(FlatTenOff()).calculate_total(), 290)

    def test_order_contains_no_discount_if_elif_logic(self):
        # Parse the real code (not the comments): no if/elif anywhere in the discount path
        for method in (Order.calculate_total, Order.set_discount):
            tree = ast.parse(textwrap.dedent(inspect.getsource(method)))
            if_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.If)]
            self.assertEqual(if_nodes, [], f"{method.__name__} contains an if/elif")
        self.assertNotIn("discount_type", inspect.getsource(Order))


if __name__ == "__main__":
    unittest.main()
