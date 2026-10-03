import os
import json

FILE_NAME = "inventory.json"


# Persistence
def load_inventory():
    """Load inventory.json if it exists, otherwise start empty."""
    if not os.path.exists(FILE_NAME):
        print("No inventory file found. Starting with an empty inventory.")
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            stocks = json.load(file)
        print("Inventory loaded successfully from inventory.json.")
        return stocks
    except (json.JSONDecodeError, IOError):
        print("Error loading JSON file. Starting with empty inventory.")
        return []


def save_inventory(stocks):
    """Save the whole inventory list to inventory.json."""
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(stocks, file, indent=4)
    print("Inventory saved to inventory.json.")



# Helpers (small, reusable pieces)
def find_product(stocks, product_id):
    """Return the product dict with this ID, or None if not found."""
    for product in stocks:
        if product["id"] == product_id:
            return product
    return None


def read_stock_quantity(prompt):
    """Ask for a non-negative whole number. Returns None if invalid."""
    try:
        quantity = int(input(prompt))
    except ValueError:
        print("Invalid input. Stock must be a whole number.")
        return None
    if quantity < 0:
        print("Stock quantity cannot be negative.")
        return None
    return quantity


def read_price(prompt):
    """Ask for a non-negative price. Returns None if invalid."""
    try:
        price = float(input(prompt))
    except ValueError:
        print("Invalid input. Price must be a number.")
        return None
    if price < 0:
        print("Price cannot be negative.")
        return None
    return price


def create_product(product_id, name, price, stock):
    """Build a product dictionary."""
    return {
        "id": product_id,
        "Product_name": name,
        "Price": price,
        "Stock": stock,
    }


def format_row(product):
    """Format one product as a table row."""
    return (
        f"{product['id']: <10} {product['Product_name']: <20} "
        f"{product['Stock']: <10} {product['Price']: <10.2f}"
    )



# Core features
def add_product(stocks):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()

    # Checking for dupes
    if find_product(stocks, product_id):
        print(f"Error: Product ID '{product_id}' already exists.")
        return

    product_name = input("Product Name: ").strip()

    #Function read_stock_quantity checks validity of stock
    quantity = read_stock_quantity("Stock Quantity: ")
    if quantity is None:
        return

    #Function read_price checks validity of price
    price = read_price("Price($): ")
    if price is None:
        return

    #Add in the new product to the list in dictionary format
    stocks.append(create_product(product_id, product_name, price, quantity))
    print(f"Product '{product_name}' added successfully.")


def update_stock(stocks):
    product_id = input("Enter Product ID: ").strip()
    product = find_product(stocks, product_id)

    #Check if product exists
    if product is None:
        print(f"Product ID '{product_id}' not found in the inventory.")
        return

    new_stock = read_stock_quantity(
        f"Current stock for {product['Product_name']} is {product['Stock']}. "
        "Enter new stock quantity: "
    )
    if new_stock is None:
        return

    product["Stock"] = new_stock
    print(f"Stock for {product['Product_name']} has been updated to {new_stock}.")


def search_product(stocks):
    product_id = input("Enter Product ID: ").strip()
    product = find_product(stocks, product_id)

    if product:
        display_all([product])
    else:
        print("No matching products found.")


def display_all(stocks):
    if len(stocks) == 0:
        print("\nThe inventory is currently empty.")
        return

    print("\n Current Inventory")
    print("=" * 55)
    print(f"{'ID': <10} {'Product': <20} {'Stock': <10} {'Price': <10}")
    print("-" * 55)
    for product in stocks:
        print(format_row(product))
    print("=" * 55)



# Menu
def print_menu():
    print("\n===== Menu =====")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")


def main():
    products = load_inventory()

    # Menu choice -> function. Each takes the products list.
    actions = {
        "1": display_all,
        "2": add_product,
        "3": update_stock,
        "4": search_product,
        "5": save_inventory,
    }

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "6":
            save_inventory(products)  # auto-save on exit
            print("Goodbye!")
            break

        action = actions.get(choice)
        if action:
            action(products)
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()