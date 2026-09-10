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

    exit = input("\nPlease enter stock quantity or type 'quit' to exit: ")

