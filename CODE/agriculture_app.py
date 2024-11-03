import tkinter as tk
from tkinter import ttk, messagebox
from crop_database import match_crops, backyard_crops_data
from input_handler import get_month_input
import os
import tkintermapview
import requests

# Define the API key at the top level
GOOGLE_API_KEY = "AIzaSyA15taRy4gEUcA27aU0xNZu-9JgMEkXflo"

class AgricultureApp:
    def __init__(self):
        self.root = None
        self.current_lat = None
        self.current_lng = None
        self.map_widget = None
        
    def get_location_from_zip(self, zip_code):
        """Get location coordinates from zip code using Google Geocoding API"""
        url = f"https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': f"{zip_code}, USA",  # Adding USA to improve accuracy
            'key': GOOGLE_API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        return None, None
        
    def start_ui(self):
        self.root = tk.Tk()
        self.root.title("Enhanced Crop Suggestion App")
        self.root.geometry("1200x800")
        
        # Create main container
        self.main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.create_input_frame()
        self.create_map_frame()
        return self.root
    
    def create_input_frame(self):
        input_frame = ttk.Frame(self.main_container, width=400)
        self.main_container.add(input_frame, weight=1)

        # Add title
        title_label = ttk.Label(input_frame, text="Crop Planner", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=10)

        # Month selection
        month_frame = ttk.LabelFrame(input_frame, text="Month Selection", padding=5)
        month_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.month_var = tk.StringVar(value="January")
        month_names = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
        month_dropdown = ttk.Combobox(
            month_frame,
            textvariable=self.month_var,
            values=month_names
        )
        month_dropdown.pack(fill=tk.X, padx=5, pady=5)

        # Location selection frame
        location_frame = ttk.LabelFrame(input_frame, text="Location Selection", padding=5)
        location_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Current location display
        self.location_label = ttk.Label(location_frame, text="No location selected")
        self.location_label.pack(pady=2)
        
        # Zip code entry
        zip_frame = ttk.Frame(location_frame)
        zip_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(zip_frame, text="Enter Zip Code:").pack(side=tk.LEFT, padx=5)
        self.zip_entry = ttk.Entry(zip_frame, width=10)
        self.zip_entry.pack(side=tk.LEFT, padx=5)

        # Search button
        search_btn = ttk.Button(
            location_frame,
            text="Search by Zip Code",
            command=self.handle_search
        )
        search_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Map instructions
        ttk.Label(location_frame, 
                 text="Or click anywhere on the map to select location",
                 wraplength=350).pack(pady=5)

        # Results area
        results_frame = ttk.LabelFrame(input_frame, text="Crop Suggestions", padding=5)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Set wrap to tk.WORD to wrap at word boundaries
        self.results_text = tk.Text(results_frame, height=20, width=40, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_map_frame(self):
        map_frame = ttk.Frame(self.main_container)
        self.main_container.add(map_frame, weight=2)

        # Create map widget
        self.map_widget = tkintermapview.TkinterMapView(
            map_frame, 
            width=800, 
            height=600, 
            corner_radius=0
        )
        self.map_widget.pack(fill=tk.BOTH, expand=True)

        # Set default position (US center)
        self.map_widget.set_position(39.8283, -98.5795)
        self.map_widget.set_zoom(4)

        # Bind click event
        self.map_widget.add_left_click_map_command(self.on_map_click)

    def get_soil_type(self, lat, lng):
        """Simplified soil type determination based on latitude"""
        # This is a very simplified determination - you might want to enhance this
        if 25 <= lat <= 35:
            return "sandy"
        elif 35 < lat <= 45:
            return "well-drained"
        else:
            return "clay"

    def on_map_click(self, coords):
        self.current_lat = coords[0]
        self.current_lng = coords[1]
        self.map_widget.delete_all_marker()
        marker = self.map_widget.set_marker(coords[0], coords[1])
        
        # Update location label
        self.location_label.config(text=f"Selected: {coords[0]:.4f}, {coords[1]:.4f}")
        
        # Get soil type and update suggestions
        soil_type = self.get_soil_type(coords[0], coords[1])
        self.update_info(soil_type)

    def handle_search(self):
        zip_code = self.zip_entry.get().strip()
        if not zip_code:
            messagebox.showwarning("Input Error", "Please enter a zip code")
            return
            
        try:
            lat, lng = self.get_location_from_zip(zip_code)
            
            if lat and lng:
                self.current_lat = lat
                self.current_lng = lng
                
                # Update map
                self.map_widget.delete_all_marker()
                self.map_widget.set_position(lat, lng)
                self.map_widget.set_marker(lat, lng)
                self.map_widget.set_zoom(12)  # Zoom in when location is found
                
                # Update location label
                self.location_label.config(text=f"Selected: {zip_code}")
                
                # Get soil type and update suggestions
                soil_type = self.get_soil_type(lat, lng)
                self.update_info(soil_type)
            else:
                messagebox.showerror("Error", "Invalid zip code or location not found")
        except Exception as e:
            messagebox.showerror("Error", f"Could not process zip code: {str(e)}")

    def update_info(self, soil_type):
        try:
            # Get month index from month name
            month_names = ["January", "February", "March", "April", "May", "June",
                         "July", "August", "September", "October", "November", "December"]
            month = month_names.index(self.month_var.get()) + 1
            
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
                result = f"Crops suitable for {self.month_var.get()} ({soil_type} soil):\n\n"
                for crop in crops:
                    result += f"- {crop['name'].title()}\n  Vitamins: {', '.join(crop['vitamins'])}\n"
                self.results_text.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Error", f"Could not update crop suggestions: {str(e)}")

if __name__ == "__main__":
    app = AgricultureApp()
    root = app.start_ui()
    root.mainloop()
