i = 0
inventory = 0

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

print("\n\nTotal units processed: ", inventory)
print("Number of Failed/Rejected Entries: ", i,"\n")