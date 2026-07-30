from sqlalchemy import select
from sqlalchemy.orm import Session

from flightdb.models.fleet import AircraftType

AIRCRAFT_TYPES = [
    {
        "iata_code": "320",
        "name": "Airbus A320",
        "manufacturer": "Airbus",
        "model": "A320",
        "max_range_km": 6100,
        "cruise_speed_kmh": 840,
    },
    {
        "iata_code": "321",
        "name": "Airbus A321",
        "manufacturer": "Airbus",
        "model": "A321",
        "max_range_km": 5950,
        "cruise_speed_kmh": 840,
    },
    {
        "iata_code": "738",
        "name": "Boeing 737-800",
        "manufacturer": "Boeing",
        "model": "737-800",
        "max_range_km": 5436,
        "cruise_speed_kmh": 842,
    },
    {
        "iata_code": "77W",
        "name": "Boeing 777-300ER",
        "manufacturer": "Boeing",
        "model": "777-300ER",
        "max_range_km": 13650,
        "cruise_speed_kmh": 905,
    },
    {
        "iata_code": "789",
        "name": "Boeing 787-9 Dreamliner",
        "manufacturer": "Boeing",
        "model": "787-9",
        "max_range_km": 14140,
        "cruise_speed_kmh": 903,
    },
     {
            "iata_code": "812",
            "name": "Boeing 812-9 Dreamer",
            "manufacturer": "Boeing",
            "model": "812-9",
            "max_range_km": 14140,
            "cruise_speed_kmh": 1000,
        },
        
]


def seed_aircraft_types(db: Session) -> None:
    for data in AIRCRAFT_TYPES:
        existing = db.execute(
            select(AircraftType).where(AircraftType.iata_code == data["iata_code"])
        ).scalar_one_or_none()
        if existing is None:
            db.add(AircraftType(**data))
    db.commit()
