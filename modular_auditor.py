failed_entries = 0
inventory = 0

def get_valid_input():
    global failed_entries
    user_input = input("Please enter stock quantity or type 'quit' to exit: ")
    if user_input == "quit":
        return "quit"
    try:
        test = int(user_input)
        if test < 0:
            print("You typed a negative number, it is not valid.\n")
            failed_entries += 1
            return None  
    except ValueError:
            print("Invalid input. Please enter a valid stock quantity.\n")
            failed_entries += 1
            return None      
    return int(user_input)

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
    print("Total amount to be paid: $", f"{total_inventory + calculate_tax(total_inventory):.2f}", "\n")

while True:
    result = get_valid_input()
    if result == "quit":
        break
    if result is None:
        continue

    if inventory + result > 500:
        print("\nThis would exceed the total inventory: ", inventory)
        break

    inventory = process_delivery(inventory, result)
    print("Current delivery processed: ", inventory)

    if inventory == 500:
       print("\nYou have reached the maximum total inventory: ", inventory)
       break

generate_report(inventory, failed_entries)