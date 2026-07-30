from sqlalchemy import select
from sqlalchemy.orm import Session

from flightdb.models.fleet import AircraftType, CabinLayout

CABIN_LAYOUTS = [
    {"type_iata": "320", "name": "standard", "total_seats": 180},
    {"type_iata": "320", "name": "two-class", "total_seats": 150},
    {"type_iata": "321", "name": "standard", "total_seats": 220},
    {"type_iata": "321", "name": "two-class", "total_seats": 185},
    {"type_iata": "738", "name": "standard", "total_seats": 189},
    {"type_iata": "738", "name": "two-class", "total_seats": 162},
    {"type_iata": "77W", "name": "three-class", "total_seats": 350},
    {"type_iata": "789", "name": "two-class", "total_seats": 290},
]


def seed_cabin_layouts(db: Session) -> None:
    for data in CABIN_LAYOUTS:
        aircraft_type = db.execute(
            select(AircraftType).where(AircraftType.iata_code == data["type_iata"])
        ).scalar_one()

        existing = db.execute(
            select(CabinLayout).where(
                CabinLayout.aircraft_type_id == aircraft_type.id,
                CabinLayout.name == data["name"],
            )
        ).scalar_one_or_none()
        if existing is not None:
            continue

        db.add(CabinLayout(
            aircraft_type_id=aircraft_type.id,
            name=data["name"],
            total_seats=data["total_seats"],
        ))
    db.commit()
