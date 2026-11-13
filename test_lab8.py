"""Lab 8 demonstrations. Write your 'Predict first' answers BEFORE running each section.
Run:  python test_lab8.py
"""
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier
from inventory import Inventory
from order import Order


def show_product_details(product: Product) -> None:
    """Works for ANY Product (LSP): uses only what Product promises."""
    product.display_information()
    print(product.get_fulfilment_info())


def section(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ---------------------------------------------------------------
section("2. ASSOCIATION: Supplier and Product")
supplier = Supplier("S100", "Acme Supply", "orders@acme.com")
laptop = PhysicalProduct("T1", "Test Laptop", 1000.0, 5, supplier, 2.0)
ebook = DigitalProduct("T2", "Test Ebook", 10.0, 5, supplier, 50.0)

laptop.get_supplier().display_information()
ebook.get_supplier().display_information()
print("Same Supplier object shared by both products?",
      laptop.get_supplier() is ebook.get_supplier())

del supplier
print("\nAfter `del supplier`:")
laptop.get_supplier().display_information()
ebook.get_supplier().display_information()

# ---------------------------------------------------------------
section("3. AGGREGATION: Inventory and Product")
inv_a = Inventory()
inv_b = Inventory()
inv_a.add_product(laptop)                      # product existed BEFORE any inventory
print("In A:", [p.get_name() for p in inv_a.get_products()])

removed = inv_a.remove_product("T1")
print("Removed from A:", removed.get_name() if removed else None)
print("A now:", [p.get_name() for p in inv_a.get_products()])
print("Product still usable:")
laptop.display_information()

inv_b.add_product(laptop)                      # transfer to B
print("In B:", [p.get_name() for p in inv_b.get_products()])
print("Same object in B as the original?", inv_b.find_product("T1") is laptop)

# ---------------------------------------------------------------
section("4. COMPOSITION: Order and OrderLine")
order1 = Order("O1")
order1.add_order_line(laptop, 2)
order1.add_order_line(ebook, 3)
order1.display_information()

order2 = Order("O2")
order2.add_order_line(laptop, 1)               # same Product, different Order

line_in_1 = order1.get_order_lines()[0]
line_in_2 = order2.get_order_lines()[0]
print("\nOrderLine objects equal?  ", line_in_1 is line_in_2)
print("Product objects equal?    ", line_in_1.get_product() is line_in_2.get_product())
print("Order 1 lines / Order 2 lines:",
      len(order1.get_order_lines()), "/", len(order2.get_order_lines()))

order1.remove_order_line("T2")
print("\nAfter removing the ebook line from Order 1:")
order1.display_information()
print("Ebook product still exists:", ebook.get_name())

# ---------------------------------------------------------------
section("6/7. LSP + POLYMORPHISM through the Product type")
inventory = Inventory()
supplier2 = Supplier("S200", "Beta Corp", "hi@beta.com")
inventory.add_product(PhysicalProduct("P1", "Keyboard", 45.0, 25, supplier2, 0.8))
inventory.add_product(DigitalProduct("P2", "Antivirus", 30.0, 100, supplier2, 350.0))

print("show_product_details() with each product type:")
for p in inventory.get_products():             # one loop, no isinstance()
    show_product_details(p)
    print("  update_stock(50) ->", p.update_stock(50), "| stock now", p.get_stock())
    print("  update_stock(-1) ->", p.update_stock(-1), "| stock now", p.get_stock())

# ---------------------------------------------------------------
section("5. TYPE HINTS evidence")
print("Inventory.find_product:", Inventory.find_product.__annotations__)
print("Inventory.add_product :", Inventory.add_product.__annotations__)
print("Product.__init__      :", Product.__init__.__annotations__)
print("Order.add_order_line  :", Order.add_order_line.__annotations__)