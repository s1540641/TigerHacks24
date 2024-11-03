import tkinter as tk
from tkinter import ttk
import webbrowser
import folium
from crop_database import match_crops, backyard_crops_data
from input_handler import get_month_input
import tempfile
GOOGLE_API_KEY = "AIzaSyA15taRy4gEUcA27aU0xNZu-9JgMEkXflo"
import os
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

class AgricultureApp: #makes the main class
    def __init__(self, google_services):
        self.google_services = google_services #handles api things
        self.root = None 
        self.map_widget = None
        self.current_lat = None #latitude for map 
        self.current_lng = None #longitude for map
        self.temp_html = None  #stores the html for the map
    
    def start_ui(self): #starts Ui
        self.root = tk.Tk()
        self.root.title("Enhanced Crop Suggestion App")
        self.root.geometry("800x600") #default window size so its not random
        self.create_input_frame() # left side takes inputs and controls 
        self.create_map_frame() #right size of screen- displays map
        return self.root
    
    def create_input_frame(self):
        #makes input fram on the left side
        input_frame = ttk.Frame(self.root)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        #creates month slection dropdown
        self.month_var = tk.StringVar(value="1") #defult is jan
        ttk.Label(input_frame, text="Select Month:").pack()
        month_dropdown = ttk.Combobox(
            input_frame,
            textvariable=self.month_var,
            values=[str(i) for i in range(1, 13)] # 12 months
        )
        month_dropdown.pack()

        #where you can enter your zip code 
        ttk.Lable(input_frame, text="Enter Zip Code:").pack()
        self.zip_entry = ttk.Entry(input_frame)
        self.zip_entry.pack()

        #search button
        ttk.Button(
            input_frame,
            text="Search",
            command=self.handle_search 
        ).pack(pady=10)

        self.results_text = tk.Text(input_frame, height=10, width=40)
        self.results_text.pack()

    def create_map_frame(self):#creates the frame that will display the map
        self.map_frame = ttk.Frame(self.root)
        self.map_frame.pack(side = tk.RIGHT, fill = tk.BOTH, expand = True)
        self.initialize_map()#initilize map to default location

    def initialize_map(self, lat=40.7128, lng=-74.0060):
        m = folium.Map(location= [lat, lng], zoom_start=12)
        self.temp_html = tempfile.NamedTemporaryFile(delete = False, suffix = '.html')
        #created a temporatry file to store the html
        m.save(self.temp_html.name)
        self.display_map() #displays the inital map
    
    def handle_search(self):
        zip_code = self.zip_entry.get()
        # location from zip code
        lat, lng = self.google_services.get_location_data(zip_code)
        if lat and lng:
            self.current_lat = lat
            self.current_lng = lng 
            # get and analyze spil data for the location
            soil_image = self.google_services.get_soil_data(lat, lng)
            soil_type = self.google_services.analyze_soil_from_colors(soil_image)

            self.update_map(lat, lng)#update the maps new loco
            self.update_info(soil_type)# update crop suggestions 
        else:#wrong zip code
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "invalid zip code")
    def update_info(self, soil_type):
        month = int(self.month_var.get())
        if month in [12, 1, 2]:
            season = 'winter_season'
        elif month in [3, 4, 5]:
            season = 'cool_season'
        elif month in [6, 7, 8]: 
            season = 'warm_season'
        else:
            season = 'cool_season'

        crops = match_crops(season, soil_type)
        self.results_text.delete(1.0, tk.END)
        if isinstance(crops, str):
            self.results_text.insert(tk.END, crops)
        else:
            month_name = get_month_input(month)
            result = f"Crops sutiable for {month_name} ({soil_type} soil):\n\n"
            for crop in crops:
                result += f"- {crop['name']}\n Vitamins: {', '.join(crop['vitamins'])}\n"
            self.results_text.insert(tk.END, result)
    def update_map(self, lat, lng):
        m = folium.Map(location=[lat, lng], zoom_start=12)
        folium.Marker([lat, lng]).add_to(m)
        m.save(self.temp_html.name)
        self.display_map()
    def main():
        google_services = GoogleServices('AIzaSyA15taRy4gEUcA27aU0xNZu-9JgMEkXflo') #initialize the google services key
        app = AgricultureApp(google_services)
        root = app.start_ui()
        root.mainloop()
    if __name__ == "__main__":
        main()

