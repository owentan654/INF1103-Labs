import contextlib
import io
import os
import tempfile
import unittest

from inventory import Inventory
from storage import load_products
from supplier import Supplier

SUPPLIER = Supplier("S0", "CSV Import", "import@example.com")

CSV_TEXT = """product_type,product_id,name,price,stock_quantity
physical,A1,Lamp,10.00,5
digital,B1,Editor,20.00,9
gadget,C1,Unknown Type,5.00,1
physical,D1,Bad Price,xyz,2
physical,E1
physical,A1,Duplicate Id,10.00,5
"""


def run_loader(path: str) -> tuple[Inventory, str]:
    inventory = Inventory()
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        load_products(path, inventory, SUPPLIER)
    return inventory, output.getvalue()


class LoadProductsTests(unittest.TestCase):
    def test_missing_file_is_handled_without_crashing(self):
        inventory, output = run_loader("this_file_does_not_exist.csv")
        self.assertEqual(len(inventory.get_products()), 0)
        self.assertIn("not found", output)
        self.assertIn("Load attempt finished.", output)

    def test_bad_rows_are_reported_and_skipped_but_good_rows_load(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "products.csv")
            with open(path, "w", newline="", encoding="utf-8") as file:
                file.write(CSV_TEXT)
            inventory, output = run_loader(path)
        ids = [p.get_product_id() for p in inventory.get_products()]
        self.assertEqual(ids, ["A1", "B1"])
        self.assertIn("2 products loaded.", output)
        self.assertEqual(output.count("skipped"), 4)       # unknown type, bad price, short row, duplicate
        self.assertTrue(output.rstrip().endswith("Load attempt finished."))


if __name__ == "__main__":
    unittest.main()