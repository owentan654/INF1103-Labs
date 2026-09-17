i = 0
inventory = 0

def get_valid_input(user_input, failed_entries):
    if user_input.isdigit() == False:
        print("\nInvalid input. Please enter a valid stock quantity.\n")
        failed_entries += 1
    #else:
    #    inventory += int(user_input)
    #    print("Current stock quantity: ", inventory)

    return failed_entries

def process_delivery(current_total,new_value):
    current_total += new_value
    return current_total

def calculate_tax(inventory):
    tax = 0.1 * inventory
    return tax

quit = input("Please enter stock quantity or type 'quit' to exit: ")
while quit != "quit":
   # if quit.isdigit() == False:
   #     print("\nInvalid input. Please enter a valid stock quantity.\n")
   #     i += 1
   # else:
   #     inventory += int(quit)
   #     print("Current stock quantity: ", inventory)
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

print("\n\nTotal units processed: ", inventory, "units.")
print("Number of Failed/Rejected Entries: ", i)
print("Total tax to be paid: $", f"{calculate_tax(inventory):.2f}","\n")
