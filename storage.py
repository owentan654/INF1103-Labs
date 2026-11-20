"""File handling: loading/saving the inventory and writing the report."""
import json
import os, csv

from inventory import Inventory
from product import Product
from supplier import Supplier
from product_factory import ProductFactory

FILE_NAME: str = "inventory.json"
REPORT_FILE: str = "report.txt"


def get_supplier(data: dict, suppliers: dict[str, Supplier]) -> Supplier:
    """Reuse one supplier object per supplier_id so products share it"""
    sid = data["supplier_id"]
    if sid not in suppliers:
        suppliers[sid] = Supplier(sid, data["name"], data["contact_email"])
    return suppliers[sid]


def create_product(item: dict, suppliers: dict[str,Supplier]) -> Product:
    """Delegates creation to ProductFactory (it raises ValueError for unknown types)."""
    kind = item["type"]
    supplier = get_supplier(item["supplier"], suppliers)
    extra = item["weight"] if kind == "physical" else item["download_size"]
    return ProductFactory.create(kind, item["id"], item["Product_name"],
                                 item["Price"], item["Stock"], supplier, extra)

def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Loads products from a CSV file"""
    loaded = 0
    try:
        file = open(path, newline= "")
    except FileNotFoundError:
        print(f"Prodcuts file not found: {path}")

    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip header
            for line_number, row in enumerate(reader, start = 2):
                if not row:
                    continue
                try:
                    product_type, product_id, name, price, stock = row[:5]
                    extra = float(row[5]) if len(row) > 5 else 0.0
                    product = ProductFactory.create(
                        product_type.strip(), product_id.strip(), name.strip(),
                        float(price), int(stock), supplier, extra)
                except ValueError as error:
                    print(f"Row {line_number} skipped: {error}")
                    continue
                if inventory.add_product(product):
                    loaded += 1
                else:
                    print(f"Row {line_number} skipped: ID '{product_id.strip()}' already exists.")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")

def load_inventory() -> Inventory:
    inventory = Inventory()
    if os.path.exists(FILE_NAME):
        try:
            suppliers: dict[str, Supplier] = {}
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                for item in json.load(file):
                    inventory.add_product(create_product(item, suppliers))
            print("Inventory loaded.")
        except (json.JSONDecodeError, IOError, KeyError, ValueError):
            print("Error loading file. Starting empty.")
            return Inventory()
    else:
        print("No file found. Using default products.")
        techsource = Supplier("S001", "TechSource", "sales@techsource.com")
        softworks = Supplier("S002", "SoftWorks", "hello@softworks.com")
        inventory.add_product(ProductFactory.create("physical", "P001", "Laptop", 1200.00, 15, techsource, 2.0))
        inventory.add_product(ProductFactory.create("physical", "P002", "Mouse", 25.50, 40, techsource, 0.1))
        inventory.add_product(ProductFactory.create("digital", "P003", "Antivirus", 45.00, 25, softworks, 350))
    return inventory


def save_inventory(inventory: Inventory) -> None:
    data = [p.to_dict() for p in inventory.get_products()]
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent = 4)
    print("Inventory saved.")


def generate_report(inventory: Inventory, failed_entries: int) -> None:
    lines = [
        "=" * 30,
        "Final Report:",
        "=" * 30,
        f"Total units processed: {inventory.get_total_units()} units.",
        f"Number of Failed/Rejected Entries: {failed_entries}",
        f"Total tax to be paid: ${inventory.calculate_tax():.2f}",
        "=" * 30,
    ]
    report = "\n".join(lines)
    print("\n" + report)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report + "\n")
    print(f"\nReport saved to {REPORT_FILE}")