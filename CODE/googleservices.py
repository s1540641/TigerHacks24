
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.cloud import vision
import requests
import os
import json
import tempfile
from PIL import Image
import numpy as np

class GoogleServices:
    def __init__(self, api_key):
        self.api_key = api_key
        self.places_client = build('places', 'v1', credentials=Credentials(None))
        self.vision_client = vision.ImageAnnotatorClient()
        
    def get_location_data(self, zip_code):
        """Get location coordinates from zip code using Google Places API"""
        url = f"https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': zip_code,
            'key': self.api_key
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        return None, None

    def get_weather_info(self, lat, lng):
        """Get weather information using Google Places API"""
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            'location': f"{lat},{lng}",
            'radius': '1000',
            'type': 'weather',
            'key': self.api_key
        }
        response = requests.get(url, params=params)
        return response.json()

    def get_soil_data(self, lat, lng):
        """Get soil data using Maps Static API"""
        url = f"https://maps.googleapis.com/maps/api/staticmap"
        params = {
            'center': f"{lat},{lng}",
            'zoom': 18,
            'size': '640x640',
            'maptype': 'satellite',
            'key': self.api_key
        }
        response = requests.get(url, params=params)
        
        # Save satellite image temporarily
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            tmp_file.write(response.content)
            return tmp_file.name

    def analyze_soil_from_colors(self, image_path):
        """Analyze soil types based on image colors using Vision API"""
        with open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = self.vision_client.image_properties(image=image)
        properties = response.image_properties_annotation

        # Analyze dominant colors to determine soil type
        dominant_colors = [color.color for color in properties.dominant_colors.colors]
        return self._classify_soil_type(dominant_colors)

    def _classify_soil_type(self, colors):
        """Helper method to classify soil type based on color analysis"""
        # Simple classification based on RGB values
        # This is a basic implementation - you might want to enhance it
        soil_types = {
            'well-drained': ((139, 69, 19), (160, 82, 45)),  # Brown colors
            'clay': ((178, 34, 34), (165, 42, 42)),          # Red-brown colors
            'sandy': ((210, 180, 140), (245, 245, 220))      # Light brown/beige colors
        }
        
        # Compare dominant colors with soil type references
        for color in colors[:3]:  # Check top 3 dominant colors
            rgb = (color.red, color.green, color.blue)
            for soil_type, ranges in soil_types.items():
                if self._color_in_range(rgb, ranges[0], ranges[1]):
                    return soil_type
        
        return 'well-drained'  # Default soil type

    def _color_in_range(self, color, range_min, range_max):
        """Helper method to check if a color falls within a specified range"""
        return all(range_min[i] <= color[i] <= range_max[i] for i in range(3))
