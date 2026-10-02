import os
import json

FILE_NAME = "inventory.json"
failed_entries = 0
inventory = 0

#Check inventory and create if it doesn't exist
def load_inventory():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding = "utf-8") as file:
                inventory = json.load(file)
                print("Inventory loaded successfully from inventory.json.")
                return inventory
        except (json.JSONDecodeError, IOError):
            print("Error loading JSON file. Starting with empty inventory.")
            return []
    else:
        print("No inventory file found. Initializing with default products.")
        return[
            {"id": "1001", "Product_name": "Laptop", "Price": 1200.00, "Stock": 15},
            {"id": "1002", "Product_name": "Mouse", "Price": 25.50, "Stock": 40},
            {"id": "1003", "Product_name": "Keyboard", "Price": 45.00, "Stock": 25},          
        ]

#Saves new orders to json file
def save_inventory(order):
    with open(FILE_NAME, "a", encoding = "utf-8") as file:
        json.dump(order, file)
        file.write("\n") 

def add_product(stocks):
    print("Add New Product")
    product_id = input("Product ID: ").strip()

    #Checking for dupes
    for items in stocks:
        if items["id"] == product_id:
            print(f"Error: Product ID '{product_id}' already exists.")
            return "Dupe"

    product_name = input("Product Name: ").strip()

    try:
        items = int(input("Stock Quantity: "))
        price = float(input("Price($): ")) 
        if items < 0 or price < 0:
            print("Stock and Price must be above 0. Please try again.")
            return "Invalid"
    except ValueError:
        print("Invalid input. Stock must be an integer and price a number. Please try again.")
        return None

    #Store new product in a dictionary
    new_product = {
        "id": product_id,
        "Product_name": product_name,
        "Price": price,
        "Stock": items
    }
    stocks.append(new_product)
    print(f"Product '{product_name}' added successfully.")
    #with open(FILE_NAME, "a", encoding = "utf-8") as file:
    #    json.dump(new_product, file)
    #    file.write("\n")

def update_stock(orders):
    product_id = input("Enter Product ID: ").strip()
    for product in orders:
        if product["id"] == product_id:
            try:
                new_stock = int(input(
                    f"Current stock for {product['Product_name']} is {product['Stock']}.Enter new stock quantity: "
                    )
                )
                if new_stock < 0:
                    print("Stock quantity cannot be negative. Please key in a positive value.")
                    return
                product["Stock"] = new_stock
                print(f"Stock for {product['Product_name']} has been updated to {new_stock}.")
                return
            except ValueError:
                print("Invalid stock quantity entered.")
                return
    print(f"Product ID '{product_id}' not found in the inventory.")

def search_product(item):
    item_name = input("Enter Product ID: ").strip()
    results = [
        items
        for items in item
        if item_name == item["id"]
    ]
#Display inventory
def display_all(inventory):
    if len(inventory) == 0:
        print("\nThe inventory is currently empty.")
        return

    print("\n" + "="*55)
    for stuff in inventory:
        print(
            f"{stuff['id']: <10} {stuff['Product_name']: <20} {stuff['Stock']: <10} {stuff['Price']: <10.2f}"
        )
    print("\n" + "="*55)
    
def get_valid_input():
    global failed_entries
    product_name = input("\nEnter Product Name: ")
    if product_name == "quit":
            return "quit"
    qty_input = input("Enter Quantity: ")
    if qty_input == "quit":
        return "quit"
    try:
        test = int(qty_input)
        if test < 0:
            print("You typed a negative number, it is not valid.\n")
            failed_entries += 1
            return None  
    except ValueError:
            print("Invalid input. Please enter a valid stock quantity.\n")
            failed_entries += 1
            return None      
    return str(product_name), int(qty_input)

def process_delivery(current_total, new_value):
    current_total += new_value
    if current_total > 500:
        return None
    return current_total

def calculate_tax(inventory):
    tax = 0.1 * inventory
    return tax

def generate_report(total_inventory, failed_entries, orders):
    print("\n\nTotal units processed: ", total_inventory, "units.")
    print("Number of Failed/Rejected Entries: ", failed_entries)
    print("Total tax to be paid: $", f"{calculate_tax(total_inventory):.2f}")
    #Rewrite the whole inventory.txt file with the final report
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        for order in orders:
            file.write(f"{order[0]},{order[1]},{order[2]}\n")
        file.write("\n\n==============================\nFinal Report:\n==============================\n")
        file.write(f"Total units processed: {total_inventory} units.\n")
        file.write(f"Number of Failed/Rejected Entries: {failed_entries}\n")
        file.write(f"Total tax to be paid: ${calculate_tax(total_inventory):.2f}\n")
        file.write("==============================\n")
    display_all(orders)
    print("\nInventory report saved to inventory.txt")
            
#load_inventory()
products = load_inventory()
for product in products:
    inventory += product[2]
print("To exit the program, type 'quit'.\n")

while True:

    display_all(products)

    result = get_valid_input()
    if result == "quit":
        break
    if result is None:
        continue

    if process_delivery(inventory, result[1]) is None:
        print("Inventory limit exceeded 500.")
        break

    #To check serial number for new orders, and make sure it starts from 1001
    if products:
        serial_number = products[-1][0] + 1
    else:
        serial_number = 1001
    new_order = (serial_number, result[0], result[1])
    products.append(new_order)
    inventory = process_delivery(inventory, result[1])

    save_inventory(new_order)

    print("\nNew Order Added: ")
    print(*new_order, sep = ", ")
    print("\n\nOrder successfully saved to inventory.txt")

generate_report(inventory, failed_entries, products)