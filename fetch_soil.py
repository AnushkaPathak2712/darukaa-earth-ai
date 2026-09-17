import requests
import json
import os

# Ensure directory exists
os.makedirs('data/structured', exist_ok=True)

# Coordinates (Semi-arid region in India)
lat = 26.5
lon = 80.5

# SoilGrids API endpoint
url = f"https://rest.isric.org/soilgrids/v2.0/properties/query?lon={lon}&lat={lat}&property=phh2o&property=soc&depth=0-5cm&value=mean"

print(f"Fetching soil data for lat={lat}, lon={lon}...")
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    with open('data/structured/soil_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Success! Data saved to data/structured/soil_data.json")
else:
    print(f"Error: {response.status_code}")