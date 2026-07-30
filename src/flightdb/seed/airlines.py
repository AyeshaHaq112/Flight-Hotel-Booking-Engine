from sqlalchemy import select
from sqlalchemy.orm import Session

from flightdb.models.geography import Airline

AIRLINES = [
    {"iata_code": "PK", "icao_code": "PIA", "name": "Pakistan International Airlines", "country": "PK"},
    {"iata_code": "EK", "icao_code": "UAE", "name": "Emirates", "country": "AE"},
    {"iata_code": "QR", "icao_code": "QTR", "name": "Qatar Airways", "country": "QA"},
    {"iata_code": "TK", "icao_code": "THY", "name": "Turkish Airlines", "country": "TR"},
    {"iata_code": "SV", "icao_code": "SVA", "name": "Saudia", "country": "SA"},
]


def seed_airlines(db: Session) -> None:
    for data in AIRLINES:
        existing = db.execute(
            select(Airline).where(Airline.iata_code == data["iata_code"])
        ).scalar_one_or_none()
        if existing is None:
            db.add(Airline(**data))
    db.commit()
