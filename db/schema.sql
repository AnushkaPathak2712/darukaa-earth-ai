CREATE TABLE IF NOT EXISTS sites (
    id INTEGER PRIMARY KEY,
    name TEXT,
    lat REAL,
    lon REAL,
    region TEXT,
    soil_ph REAL,
    organic_carbon_pct REAL,
    moisture TEXT,
    land_use TEXT,
    rainfall_mm REAL,
    temp_c REAL,
    species_richness INTEGER,
    habitat_diversity TEXT,
    pollution_level TEXT,
    deforestation_rate TEXT
);

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    title TEXT,
    source TEXT,
    year INTEGER,
    url TEXT,
    text TEXT,
    embedding_id TEXT
);

CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY,
    practice TEXT,
    metrics_improved TEXT,
    time_horizon TEXT,
    confidence TEXT,
    evidence TEXT,
    source_ids TEXT
);