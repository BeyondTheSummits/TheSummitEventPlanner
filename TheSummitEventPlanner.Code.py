#Event Planner

#Assigning Global and other variables
total_cost = 0
venue_cost = 0
staff_cost = 0
catering_cost = 0
entertainment_cost = 0
insurance_cost = 0
production_cost = 0
logistics_cost = 0
other_cost = 0
user_restart = ""
running = True

#function to get indivitual costs
def get_cost(message):
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Invalid. Try again with a numerical value.")
#Loop for restart options
while running == True:
    #Greeeting
    print("")
    print("Welcome to the event planning application.")
    print("We will help you to caclculate your cost in regard to your budget,")
    #Request to initialise
    print("")
    user_approval = str(input("Are you ready to start the calculation? ")).lower()
    if (user_approval == "yes" ):
            print("")
            print("Perfect, Lets get started")
            #Initialising inputs with validations
            print("")
            while True:
                try:
                    userbudget = float(input("Please enter your budget: "))
                    break
                except ValueError:
                    print("Invalid. Try again with a numerical value.")
            
            print("")
            print("Your budget is ", userbudget)
            print("")
            print("Lets get started with the costs ")
            print("")
            print("Please enter the costs, if you dont have a specific cost, enter 0")
            print("")
            venue_cost = get_cost("Please enter your venue cost: ")
            staff_cost = get_cost("Please enter your staff cost: ")
            catering_cost = get_cost("Please enter your catering cost: ")     
            entertainment_cost = get_cost("Please enter your entertainment cost: ")
            production_cost = get_cost("Please enter your production cost: ")
            logistics_cost = get_cost("Please enter your logistics cost: ")
            insurance_cost = get_cost("Please enter your insurance cost: ")
            other_cost = get_cost("Please enter any other amount of cost: ")
            #Calculations and outputs
            total_cost = venue_cost + staff_cost + catering_cost + entertainment_cost + insurance_cost + production_cost + logistics_cost + other_cost
            print("")
            print("Your total cost is: ", total_cost)
            print("")
            print("Now we will compare your budget with your cost")
            if (userbudget == total_cost):
                print("")
                print("Your cost is exactly what your budget is.")
            elif (userbudget > total_cost):
                print("")
                print("Your cost is under the budget.")
                leftover = userbudget - total_cost
                print("")
                print("You have", leftover, "remaining.")
            else:
                print("")
                print("You cost is over the budget")
                over = total_cost - userbudget
                print("")
                print("You went over by", over)
            print("")
            #Restart option
            user_restart = str(input("Would you like to calculate again? ")).lower()
            if user_restart == "yes":
                print("")
                continue
            elif user_restart == "no":
                print("You can always come back.")
                break
            else:
                print("Invalid input. Closing Program")
                break
    elif user_approval == "no":
        print("You can always come back")
        break
    else:
        print("Please give a valid input")
        continue
