"""File handling: loading/saving the inventory and writing the report."""
import json
import os

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

FILE_NAME = "inventory.json"
REPORT_FILE = "report.txt"


def create_product(item):
    """Factory: reads the saved 'type' and builds the matching subclass."""
    kind = item["type"]
    if kind == "physical":
        return PhysicalProduct(item["id"], item["Product_name"],
                               item["Price"], item["Stock"], item["weight"])
    elif kind == "digital":
        return DigitalProduct(item["id"], item["Product_name"],
                              item["Price"], item["Stock"], item["download_size"])
    raise ValueError(f"Unknown product type: {kind}")


def load_inventory():
    inventory = Inventory()
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                for item in json.load(file):
                    inventory.add_product(create_product(item))
            print("Inventory loaded.")
        except (json.JSONDecodeError, IOError, KeyError, ValueError):
            print("Error loading file. Starting empty.")
            return Inventory()
    else:
        print("No file found. Using default products.")
        inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.0))
        inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, 0.1))
        inventory.add_product(DigitalProduct("P003", "Antivirus", 45.00, 25, 350))
    return inventory


def save_inventory(inventory):
    data = [p.to_dict() for p in inventory.get_products()]
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print("Inventory saved.")


def generate_report(inventory, failed_entries):
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
