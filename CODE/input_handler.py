# input_handler.py
def get_month_input(month_select=None):
    months = [
        None, "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    if month_select is None:
        # Console input
        while True:
            try:
                month_select = int(input("Enter the month as a number 1-12: "))
                if 1 <= month_select <= 12:
                    month = months[month_select]
                    confirm = input(f"You entered {month}. Is this correct? (yes/no): ").strip().lower()
                    if confirm == 'yes':
                        return month_select
                    else:
                        print("Let's try again.")
                else:
                    print("Input invalid, please try again.")
            except ValueError:
                print("Please enter a valid number.")
    else:
        # Return month directly for GUI
        return months[month_select] if 1 <= month_select <= 12 else None
