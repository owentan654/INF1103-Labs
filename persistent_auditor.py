failed_entries = 0
inventory = 0

'''def load_inventory():
    global inventory
    try:
        with open("orders.txt", "r") as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1]
                if "Total units processed:" in last_line:
                    inventory = int(last_line.split(":")[1].strip().split()[0])
    except FileNotFoundError:
        print("orders.txt not found. Starting with an empty inventory.")
        inventory = 0'''

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
    return int(qty_input), str(product_name)

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
    print("Current Order: ", products)

#load_inventory()
products = []
print("To exit the program, type 'quit'.\n")
while True:
    result = get_valid_input()
    if result == "quit":
        break
    if result is None:
        continue

    '''if inventory + result[0] > 500:
        print("\nThis would exceed the total inventory: ", inventory)
        break'''

    length = 1001 + len(products)
    products.append((length, result[1], result[0]))

    inventory = process_delivery(inventory, result[0])
    print("New Order Added: ")
    for product in products: 
        print (*product, sep = ",")
    print("Order successfully saved to orders.txt")

    '''if inventory == 500:
       print("\nYou have reached the maximum total inventory: ", inventory)
       break'''

generate_report(inventory, failed_entries)