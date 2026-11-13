from inventory import Inventory
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from order import Order
from storage import load_inventory, save_inventory, generate_report


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
            pid = input("Product ID: ").strip()
            name = input("Product name: ").strip()
            try:
                price = float(input("Price: "))
                stock = int(input("Stock: "))
                if kind == "1":
                    extra = float(input("Weight (kg): "))
                else:
                    extra = float(input("Download size (MB): "))
                if price < 0 or stock < 0 or extra < 0:
                    raise ValueError
            except ValueError:
                print("Invalid input entered. "
                      "Values must be non-negative numbers.")
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
                suppliers[sid] = supplier

            if kind == "1":
                product = PhysicalProduct(pid, name, price, stock, supplier, extra)
            else:
                product = DigitalProduct(pid, name, price, stock, supplier, extra)
            if inventory.add_product(product):
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
                order.add_order_line(product, qty)
            if order.get_orderlines():
                order.display_information()
            else:
                print("Empty order discarded.")        

        elif choice == "7":
            save_inventory(inventory)

        elif choice == "8":
            generate_report(inventory, failed_entries)
            break

        else:
            print("Invalid choice.")
            failed_entries += 1


if __name__ == "__main__":
    main()
