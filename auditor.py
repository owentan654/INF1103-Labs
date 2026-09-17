i = 0
inventory = 0

<<<<<<< HEAD
exit = input("Please enter stock quantity or type 'quit' to exit: ")
while exit != "quit":
    if exit.isdigit() == False:
        print("\nInvalid input. Please enter a valid stock quantity.\n")
        i += 1
    else:
        inventory += int(exit)
        print("Current stock quantity: ", inventory)

    if inventory > 500:
        print("\nYou have exceeded the total inventory: ", inventory)
        break
    elif(inventory == 500):
        print("\nYou have reached the maximum total inventory: ", inventory)
        break
    exit = input("\nPlease enter stock quantity or type 'quit' to exit: ")

print("\n\nTotal units processed: ", inventory, "units.")
print("Number of Failed/Rejected Entries: ", i,"\n")
=======
def get_valid_input(user_input, inventory, failed_entries):
    if user_input.isdigit() == False:
        print("\nInvalid input. Please enter a valid stock quantity.\n")
        failed_entries += 1
    else:
        inventory += int(user_input)
        print("Current stock quantity: ", inventory)

    return inventory, failed_entries

def process_delivery(current_total,new_value):
    current_total += new_value
    return current_total

exit = input("Please enter stock quantity or type 'quit' to exit: ")
while exit != "quit":
   # if exit.isdigit() == False:
   #     print("\nInvalid input. Please enter a valid stock quantity.\n")
   #     i += 1
   # else:
   #     inventory += int(exit)
   #     print("Current stock quantity: ", inventory)
   inventory, i = get_valid_input(exit, inventory, i)
   print(inventory,i)

   if inventory > 500:
        print("\nYou have exceeded the total inventory: ", inventory)
        break
   elif(inventory == 500):
        print("\nYou have reached the maximum total inventory: ", inventory)
        break
   exit = input("\nPlease enter stock quantity or type 'quit' to exit: ")

print("\n\nTotal units processed: ", inventory, "units.")
print("Number of Failed/Rejected Entries: ", i,"\n")


        
>>>>>>> 40b58a4 (Lab 3 Finished adding in valid_input functions)
