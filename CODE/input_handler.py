# Handles user input and validation

def get_month_input():
    #array of month names
    month = [
        None, "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]   
    while True:
        try:
            month_select = int(input("Enter the month as a number 1-12: ")) #prompts user to choose a month then takes their input
            if 1 <= month_select <= 12:#month will only return if input is valid
                month = month[month_select] #connects the number chosen to the month of the year
                confirm = input(f"You entered {month}. Is this correct? (yes/no): ").strip().lower()
                #only returns month if user confirms using 'yes' or 'YES'
                if confirm == 'yes':
                    return month_select
                else:
                    print("Let's try again.")
            else:
                print("input invalid, please try again")

#def get_temperature_input():