import requests
from math import radians, cos, sin, sqrt, atan2
from sqlalchemy.orm import Session
from app.db.models.geo import Location
from threading import Thread
from app.services.fraud import detect_fraud

def geocode(address: str):
    response = requests.get(f"https://nominatim.openstreetmap.org/search?q={address}&format=json")
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return float(data['lat']), float(data['lon'])
    raise ValueError("Geocoding failed")

def calculate_distance(from_addr: str, to_addr: str):
    lat1, lon1 = geocode(from_addr)
    lat2, lon2 = geocode(to_addr)
    dlon = radians(lon2) - radians(lon1)
    dlat = radians(lat2) - radians(lat1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return 6371 * c

def update_location(db: Session, courier_id: int, lat: float, lon: float):
    loc = Location(courier_id=courier_id, lat=lat, lon=lon)
    db.add(loc)
    db.commit()
    Thread(target=detect_fraud, args=(db, courier_id)).start()

def get_location_history(db: Session, courier_id: int):
    return db.query(Location).filter(Location.courier_id == courier_id).order_by(Location.timestamp).all()

def get_route(db: Session, courier_id: int):
    locations = get_location_history(db, courier_id)
    return [{"lat": loc.lat, "lon": loc.lon} for loc in locations]