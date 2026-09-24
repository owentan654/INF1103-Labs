failed_entries = 0
inventory = 0

def load_inventory():
    products = []
    try:
        with open("orders.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")

                if len(parts) == 3:
                    serial_number = int(parts[0])
                    product_name = parts[1]
                    quantity = int(parts[2])

                    products.append((serial_number, product_name, quantity))
    except FileNotFoundError:
        print("orders.txt file not found. Starting with an empty order list.")

    return products

def save_inventory(order):
    with open("orders.txt", "a") as file:
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
    return current_total

def calculate_tax(inventory):
    tax = 0.1 * inventory
    return tax

def generate_report(total_inventory, failed_entries):
    print("\n\nTotal units processed: ", total_inventory, "units.")
    print("Number of Failed/Rejected Entries: ", failed_entries)
    print("Total tax to be paid: $", f"{calculate_tax(total_inventory):.2f}")
    print("Current Order: ")
    for product in products: 
            print (*product, sep = ", ")

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

    '''if inventory + result[0] > 500:
        print("\nThis would exceed the total inventory: ", inventory)
        break'''
#No idea what is this for but ai says so
#    if products:
#        serial_number = products[-1][0] + 1
#    else:
#        serial_number = 1001

    length = 1001 + len(products)
    new_order = ((length, result[0], result[1]))
    products.append(new_order)

    inventory = process_delivery(inventory, result[1])

    save_inventory(new_order)

    print("\nNew Order Added: ")
    print(*new_order, sep = ", ")
    print("\n\nOrder successfully saved to orders.txt")

    '''if inventory == 500:
       print("\nYou have reached the maximum total inventory: ", inventory)
       break'''

generate_report(inventory, failed_entries)