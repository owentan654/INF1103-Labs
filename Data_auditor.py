failed_entries = 0
inventory = 0

#Check inventory and create if dosen't exist
def load_inventory():
    products = []
    try:
        with open("inventory.txt", "r", encoding = "utf-8") as file:
            for line in file:
                parts = line.strip().split(",")

                if parts == "==============================":
                    break

                if len(parts) == 3:
                    serial_number = int(parts[0])
                    product_name = parts[1]
                    quantity = int(parts[2])

                    products.append((serial_number, product_name, quantity))
    except FileNotFoundError:
        print("inventory.txt file not found. Starting with an empty inventory.")

    with open("inventory.txt", "a", encoding = "utf-8"):
         pass  # Create the file if it doesn't exist

    return products

def save_inventory(order):
    with open("inventory.txt", "a", encoding = "utf-8") as file:
        print(*order, sep = ",", file = file)                   

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
    with open("inventory.txt", "w", encoding="utf-8") as file:
        for order in orders:
            file.write(f"{order[0]},{order[1]},{order[2]}\n")
        file.write("\n\n==============================\nFinal Report:\n==============================\n")
        file.write(f"Total units processed: {total_inventory} units.\n")
        file.write(f"Number of Failed/Rejected Entries: {failed_entries}\n")
        file.write(f"Total tax to be paid: ${calculate_tax(total_inventory):.2f}\n")
        file.write("==============================\n")
    print("Current Order: ")
    for order in orders: 
            print (*order, sep = ", ")
    print("\nInventory report saved to inventory.txt")
            
#load_inventory()
products = load_inventory()
for product in products:
    inventory += product[2]
print("To exit the program, type 'quit'.\n")

while True:

    print("Current Orders: \n\n")
    for product in products: 
        print (*product, sep = ",")

    result = get_valid_input()
    if result == "quit":
        break
    if result is None:
        continue

#No idea what is this for but ai says so
#    if products:
#        serial_number = products[-1][0] + 1
#    else:
#        serial_number = 1001

    if process_delivery(inventory, result[1]) is None:
        print("Inventory limit exceeded 500.")
        break
    serial_number = 1001 + len(products)
    new_order = (serial_number, result[0], result[1])
    products.append(new_order)
    inventory = process_delivery(inventory, result[1])

    save_inventory(new_order)

    print("\nNew Order Added: ")
    print(*new_order, sep = ", ")
    print("\n\nOrder successfully saved to inventory.txt")

generate_report(inventory, failed_entries, products)