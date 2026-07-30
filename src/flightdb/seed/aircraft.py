from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from flightdb.models.fleet import Aircraft, AircraftType
from flightdb.models.geography import Airline

AIRCRAFT = [
    {"registration": "AP-BLS", "airline_iata": "PK", "type_iata": "320", "delivery_date": date(2015, 3, 12)},
    {"registration": "AP-BMX", "airline_iata": "PK", "type_iata": "738", "delivery_date": date(2018, 7, 20)},
    {"registration": "AP-BNL", "airline_iata": "PK", "type_iata": "77W", "delivery_date": date(2019, 11, 5)},
    {"registration": "A6-ENA", "airline_iata": "EK", "type_iata": "77W", "delivery_date": date(2016, 1, 15)},
    {"registration": "A6-ENB", "airline_iata": "EK", "type_iata": "789", "delivery_date": date(2020, 6, 1)},
    {"registration": "A7-BFA", "airline_iata": "QR", "type_iata": "789", "delivery_date": date(2021, 4, 10)},
    {"registration": "A7-BFB", "airline_iata": "QR", "type_iata": "321", "delivery_date": date(2019, 9, 22)},
    {"registration": "TC-JNA", "airline_iata": "TK", "type_iata": "321", "delivery_date": date(2017, 8, 3)},
    {"registration": "HZ-AK1", "airline_iata": "SV", "type_iata": "738", "delivery_date": date(2018, 2, 14)},
]


def seed_aircraft(db: Session) -> None:
    for data in AIRCRAFT:
        existing = db.execute(
            select(Aircraft).where(Aircraft.registration == data["registration"])
        ).scalar_one_or_none()
        if existing is not None:
            continue

        airline = db.execute(
            select(Airline).where(Airline.iata_code == data["airline_iata"])
        ).scalar_one()
        aircraft_type = db.execute(
            select(AircraftType).where(AircraftType.iata_code == data["type_iata"])
        ).scalar_one()

        db.add(Aircraft(
            registration=data["registration"],
            airline_id=airline.id,
            aircraft_type_id=aircraft_type.id,
            delivery_date=data["delivery_date"],
        ))
    db.commit()
