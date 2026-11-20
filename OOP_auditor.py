from collections.abc import Callable
from inventory import Inventory
from supplier import Supplier
from product_factory import ProductFactory
from can_be_shipped import CanBeShipped
from order import Order
from input_helpers import get_positive_float
from discount_strategy import DiscountStrategy, NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount
from storage import load_inventory, save_inventory, generate_report, load_products


DISCOUNT_OPTIONS: dict[str, tuple[str, callable[[], DiscountStrategy]]] = {
    "1": ("No discount", lambda: NoDiscount()),
    "2": ("10% off", lambda: PercentageDiscount(10)),
    "3": ("20 off orders of 200 or more", lambda: BulkDiscount(200, 20)),
    "4": ("Student 5% off", lambda: StudentDiscount()),
}

def main() -> None:
    inventory = load_inventory()
    failed_entries = 0

    suppliers: dict[str, Supplier] = {}
    for p in inventory.get_products():
        s = p.get_supplier()
        suppliers[s.get_supplier_id()] = s

    menu = [
        "Display all products",
        "Add product",
        "Update stock",
        "Search Product",
        "Remove Product",
        "Create Order",
        "Import products from CSV"
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
            kind = input("Type (1 = Physical, 2 = Digital): ").strip()
            if kind != "1" and kind != "2":
                print("Invalid product type.")
                failed_entries += 1
                continue
            product_type = "physical" if kind == "1" else "digital"
            pid = input("Product ID: ").strip()
            name = input("Product name: ").strip()
            price = get_positive_float("Price: ")
            try:
                stock = int(input("Stock: "))
                if kind == "1":
                    extra = float(input("Weight (kg): "))
                else:
                    extra = float(input("Download size (MB): "))
            except ValueError:
                print("Stock must be a whole number and the last value a number.")
                failed_entries += 1
                continue
            if inventory.exceeds_limits(stock):
                print(f"Inventory limit exceeded {Inventory.MAX_UNITS}.")
                failed_entries += 1
                continue

            sid = input("Supplier ID: ").strip()
            supplier = suppliers.get(sid)
            if supplier is None:
                sname = input("New supplier name: ").strip()
                semail = input("Supplier email: ").strip()
                supplier = Supplier(sid, sname, semail)

            try: 
                product = ProductFactory.create(product_type, pid, name, price,
                                                stock, supplier, extra)
            except ValueError as e:
                print(f"Could not create product: {e}")
                failed_entries += 1
                continue

            if inventory.add_product(product):
                suppliers.setdefault(sid, supplier)
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
                continue
            try:
                product.update_stock(qty)
            except ValueError as error:
                print(error)
                failed_entries += 1
            else:
                print("Stock updated.")
 
        elif choice == "4":
            product = inventory.search_product(input("Product ID: ").strip())
            if product:
                product.display_information()
                print(f"Fulfilment: {product.get_fulfilment_info()}")
                product.get_supplier().display_information()
                if isinstance(product, CanBeShipped):
                    print(f"Shipping cost: ${product.calculate_shipping_cost():.2f}")
            else:
                print("Product not found.")
                failed_entries += 1

        elif choice == "5":
            removed = inventory.remove_product(input("Product ID: ").strip())
            if removed is None:
                print("Product not found.")
                failed_entries += 1
            else:
                print(f"Removed '{removed.get_name()}' from the inventory "
                      "(the product object itself still exists).")

        elif choice == "6":
            order = Order(input("Order ID: ").strip())
            while True:
                pid = input("Product ID to add (blank to finish): ").strip()
                if pid == "":
                    break
                product = inventory.search_product(pid)
                if product is None:
                    print("Product not found.")
                    failed_entries += 1
                    continue
                try:
                    qty = int(input("Quantity: "))
                    if qty <= 0:
                        raise ValueError
                except ValueError:
                    print("Quantity must be a positive whole number.")
                    failed_entries += 1
                    continue
                try:
                    order.add_order_line(product, qty)
                except ValueError as error:
                    print(error)
                    failed_entries += 1
            if not order.get_orderlines():
                print("Empty order discarded.")
                continue
            print("\nDiscount: ")
            for key, (label, _) in DISCOUNT_OPTIONS.items():
                print(f"  {key}. {label}")
            pick = input("Choose a discount (blank for none): ").strip()
            if pick in DISCOUNT_OPTIONS:
                order.set_discount(DISCOUNT_OPTIONS[pick][1]())
            elif pick != "":
                print("Unknown discount; using no discount.")
                failed_entries += 1
            order.display_information()
            
        elif choice == "7":
            path = input("CSV file path (blank for products.csv): ").strip() or "products.csv"
            import_supplier = suppliers.setdefault(
                "S000", Supplier("S000", "CSV Import", "import@example.com"))
            load_products(path, inventory, import_supplier)           

        elif choice == "8":
            save_inventory(inventory)

        elif choice == "9":
            generate_report(inventory, failed_entries)
            break

        else:
            print("Invalid choice.")
            failed_entries += 1


if __name__ == "__main__":
    main()
