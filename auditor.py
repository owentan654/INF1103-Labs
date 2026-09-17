i = 0
inventory = 0

def get_valid_input(user_input, failed_entries):
    if user_input.isdigit() == False:
        print("\nInvalid input. Please enter a valid stock quantity.\n")
        failed_entries += 1
    return failed_entries

def process_delivery(current_total,new_value):
    current_total += new_value
    return current_total

def calculate_tax(inventory):
    tax = 0.1 * inventory
    return tax

def generate_report(total_inventory,failed_entries):
    print("\n\nTotal units processed: ", total_inventory, "units.")
    print("Number of Failed/Rejected Entries: ", failed_entries)
    print("Total tax to be paid: $", f"{calculate_tax(total_inventory):.2f}","\n")

quit = input("Please enter stock quantity or type 'quit' to exit: ")
while quit != "quit":
   i = get_valid_input(quit, i)
   inventory = process_delivery(inventory, int(quit) if quit.isdigit() else 0)
   print ("Current delivery processed: ", inventory)

   if inventory > 500:
        print("\nYou have exceeded the total inventory: ", inventory)
        break
   elif(inventory == 500):
        print("\nYou have reached the maximum total inventory: ", inventory)
        break
   quit = input("\nPlease enter stock quantity or type 'quit' to exit: ")

generate_report(inventory, i)