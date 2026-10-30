import json, os
FILE_NAME = "inventory.json"
REPORT_FILE = "report.txt"

class Product: 
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    #Read-only access
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_stock(self):
        return self.__stock

    def update_stock(self,quantity):
        if quantity < 0:
            return False        #Protects its own state
        self.__stock = quantity
        return True

    def display_information(self):
        print(f"{self.__product_id:<10} {self.__name:<20}"
              f"{self.__stock:<10} {self.__price:<10.2f}")

    def to_dict(self):
        return {"id": self.__product_id, "Product_name": self.__name, 
                "Price": self.__price, "Stock": self.__stock}

class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            return False        #Dupe Check
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product      #returns the Product object itself
        return None
    def display_all(self):
        if not self.__products:
            print("\nThe inventory is currently empty.")
            return
        print("\n" + "=" * 55)      #Makes lines
        for product in self.__products:
            product.display_information()       #Inventory asks each Product to show itself
        print("=" * 55)

    def get_products(self):
        return self.__products

    MAX_UNITS = 500
    TAX_RATE = 0.1
    def get_total_units(self):
        return sum(p.get_stock() for p in self.__products)
    def exceeds_limits(self, extra_units):
        return self.get_total_units + extra_units > self.MAX_UNITS

    def calculate_tax(self):
        return self.TAX_RATE * self.get_total_units

def load_inventory():
    inventory = Inventory()
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                for item in json.load(file):
                    inventory.add_product(Product(
                        item["id"], item["Product_name"],
                        item["Price"], item["Stock"]
                    ))
        except (json.JSONDecodeError, IOError, KeyError):
            print("Error loading file. Starting empty.")
    else:
        print("No file found. Using default products.")
        inventory.add_product(Product("P001", "Laptop", 1200.00, 15))
        inventory.add_product(Product("P002", "Mouse", 25.50, 40))
        inventory.add_product(Product("P003", "Keyboard", 45.00, 25))
    return inventory

def save_inventory(inventory):
    data = [p.to_dict() for p in inventory.get_products()]
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent = 4)
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

def main():
    inventory = load_inventory()
    failed_entries = 0
    menu = [
        "Display all products",
        "Add product",
        "Update stock",
        "Search Product",
        "Save Inventory",
        "Exit"
    ]

    while True:
        print("\n===== Inventory Menu =====")
        for i, item in enumerate(menu, start=1):
            print(f"{i}. {item}")
        print("==========================")
        choice = input("Choice: ").strip()

        if choice == "1":
            inventory.display_all()

        elif choice == "2":
            pid = input("Product ID: ").strip()
            name = input("Product name: ").strip()
            try:
                price = float(input("Price: "))
                stock = int(input("Stock: "))
            except ValueError:
                print("Invalid number entered.")
                continue
            if inventory.add_product(Product(pid, name, price, stock)):
                print("Product added.")
            else:
                print("That ID already exists.")
                failed_entries += 1

        elif choice == "3":
            product = inventory.search_product(input("Product ID: ").strip())
            if product is None:
                print("Product not found.")
                failed_entries += 1
                continue
            try:
                qty = int(input("New stock quantity: "))
            except ValueError:
                print("Invalid quantity.")
                failed_entries += 1
                continue
            if inventory.exceeds_limits(qty - product.get_stock()):
                print(f"Inventory limit exceeded {Inventory.MAX_UNITS}.")
                failed_entries += 1
            elif product.update_stock(qty):
                print("Stock updated.")
            else:
                print("Stock cannot be negative.")
                failed_entries += 1

        elif choice == "4":
            product = inventory.search_product(input("Product ID: ").strip())
            if product:
                product.display_information()
            else:
                print("Product not found.")
                failed_entries += 1

        elif choice == "5":
            save_inventory(inventory)

        elif choice == "6":
            generate_report(inventory, failed_entries)
            break

        else:
            print("Invalid choice.")
            failed_entries += 1

main()