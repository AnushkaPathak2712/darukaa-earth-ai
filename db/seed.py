import sqlite3
import os
import json

os.makedirs('data/structured', exist_ok=True)
json_path = 'data/structured/soil_data.json'

if not os.path.exists(json_path):
    print(f"Error: {json_path} not found. Run fetch_soil.py first.")
    exit()

with open(json_path, 'r') as f:
    soil_json = json.load(f)

ph_mean = None
soc_mean = None

try:
    layers = soil_json['properties']['layers']
    for layer in layers:
        if layer['name'] == 'phh2o':
            val = layer['depths'][0]['values']['mean']
            if val is not None:
                ph_mean = val / 10.0
        elif layer['name'] == 'soc':
            val = layer['depths'][0]['values']['mean']
            if val is not None:
                soc_mean = val / 100.0
except KeyError:
    print("Error parsing JSON structure.")

if ph_mean is None:
    print("Warning: API returned no pH data. Using default 7.0")
    ph_mean = 7.0
if soc_mean is None:
    print("Warning: API returned no SOC data. Using default 1.0")
    soc_mean = 1.0

print(f"Extracted Soil Data -> pH: {ph_mean:.2f}, SOC: {soc_mean:.2f}%")

conn = sqlite3.connect('data/structured/sites.db')
c = conn.cursor()

with open('db/schema.sql', 'r') as f:
    c.executescript(f.read())

# Clear existing data to avoid duplicates
c.execute('DELETE FROM sites')

# Insert the site with real soil data + synthetic climate/land data
c.execute('''
    INSERT INTO sites (name, lat, lon, region, soil_ph, organic_carbon_pct, moisture, land_use, rainfall_mm, temp_c, species_richness, habitat_diversity, pollution_level, deforestation_rate)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    'Delhi Sample Farm', 
    28.6, 77.2, 
    'semi-arid', 
    ph_mean, soc_mean, 
    'low', 'wheat monoculture', 
    450, 28, 
    12, 'low', 'high', 'medium'
))

conn.commit()
conn.close()
print("Database seeded successfully with real soil data and region!")