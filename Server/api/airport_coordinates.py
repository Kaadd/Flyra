# Common airport coordinates lookup
AIRPORT_COORDINATES = {
    "SFO": {"lat": 37.6213, "lng": -122.3790},  # San Francisco
    "NRT": {"lat": 35.7720, "lng": 140.3929},   # Narita
    "JFK": {"lat": 40.6413, "lng": -73.7781},  # New York JFK
    "LAX": {"lat": 34.0522, "lng": -118.2437},  # Los Angeles
    "LHR": {"lat": 51.4700, "lng": -0.4543},    # London Heathrow
    "CDG": {"lat": 49.0097, "lng": 2.5479},     # Paris Charles de Gaulle
    "DXB": {"lat": 25.2532, "lng": 55.3657},    # Dubai
    "HKG": {"lat": 22.3080, "lng": 113.9185},   # Hong Kong
    "SIN": {"lat": 1.3644, "lng": 103.9915},   # Singapore
    "ICN": {"lat": 37.4602, "lng": 126.4407},  # Seoul Incheon
    "ORD": {"lat": 41.9742, "lng": -87.9073},  # Chicago O'Hare
    "ATL": {"lat": 33.6407, "lng": -84.4277},  # Atlanta
    "DFW": {"lat": 32.8998, "lng": -97.0403},  # Dallas/Fort Worth
    "DEN": {"lat": 39.8561, "lng": -104.6737},  # Denver
    "SEA": {"lat": 47.4502, "lng": -122.3088},  # Seattle
    "BOS": {"lat": 42.3656, "lng": -71.0096},  # Boston
    "MIA": {"lat": 25.7959, "lng": -80.2870},  # Miami
    "IAH": {"lat": 29.9902, "lng": -95.3368},  # Houston
    "PHX": {"lat": 33.4342, "lng": -112.0116},  # Phoenix
    "LAS": {"lat": 36.0840, "lng": -115.1537}, # Las Vegas
}

def get_airport_coordinates(iata_code: str):
    """Get airport coordinates from IATA code."""
    if not iata_code:
        return None
    iata_code = iata_code.upper().strip()
    coords = AIRPORT_COORDINATES.get(iata_code)
    if coords:
        return (coords["lat"], coords["lng"])
    return None

