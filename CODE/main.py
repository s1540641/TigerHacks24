# Main entry point of the application
from crop_database import match_crops, backyard_crops_data
from input_handler import get_month_input
import tkinter as tk
from tkinter import messagebox

def show_suggestions():
    print("Button clicked") #for debug purpsus

    #gets selected month and soil conditions form the gui
    month_index = int(month_var.get())
    soil_condition = soil_var.get()
    print(f"Selected month: {month_index}, Soil condition: {soil_condition}") #debug statement 
    
    #convert month to season
    if month_index in[12,1,2]:
        season = 'winter_season'
    elif month_index in [3, 4, 5]:
        season = 'cool_season'
    elif month_index in [6, 7, 8]:
        season = 'warm_season'
    else:
        season = 'cool_season'
        
    crops = match_crops(season, soil_condition)
    if isinstance(crops, str): 
        result = crops
    else:
        month_name = get_month_input(month_index)
        result = f"Crops sutiable for {month_name}({soil_condition} soil):\n"
        result += "\n".join(
            f"-{crop['name']} (Vitamins: {', '.join(crop['vitamins'])})" for crop in crops
        )
            #displays the results in a popup message box
        messagebox.showinfo("Crop Suggestions", result)

            #set up the gui window
root = tk.Tk()
root.title("Crop Suggestion App")

            # Dropdown for month selection
month_var = tk.StringVar(root)
month_var.set("1") #sets defult to jan
month_label = tk.Label(root, text="Select the month:")
month_label.pack()
month_dropdown = tk.OptionMenu(root, month_var, *[str(i) for i in range(1,13)])
month_dropdown.pack()

            #dropdown for soil condition selection
soil_var = tk.StringVar(root)
soil_var.set("well-drained") #sets defalt soil selection
soil_label = tk.Label(root, text="Select soil condition:")
soil_label.pack()
soil_dropdown = tk.OptionMenu(root, soil_var, *backyard_crops_data['cool_season'].keys())
soil_dropdown.pack()

zip_code_label = tk.Label(root, text="Enter Zip Code:")
zip_code_label.pack()
zip_code_entry = tk.Entry(root)
zip_code_entry.pack()

            #creats a button to show crop suggestions
btn_suggest = tk.Button(root, text="Get Crop Suggestions", command=show_suggestions)
btn_suggest.pack()

            #starts the application
print("Starting the")
root.mainloop()