from datetime import date, time

from sqlalchemy import select
from sqlalchemy.orm import Session

from flightdb.models.fleet import AircraftType
from flightdb.models.geography import Airline, Airport
from flightdb.models.schedule import ScheduledFlight

SCHEDULED_FLIGHTS = [
    {
        "flight_number": "PK301",
        "airline_iata": "PK",
        "origin_iata": "LHE",
        "destination_iata": "KHI",
        "departure_time": time(8, 0),
        "arrival_time": time(10, 0),
        "days_of_week": [1, 2, 3, 4, 5, 6, 7],
        "type_iata": "320",
        "effective_from": date(2025, 1, 1),
        "effective_until": None,
    },
    {
        "flight_number": "PK302",
        "airline_iata": "PK",
        "origin_iata": "KHI",
        "destination_iata": "LHE",
        "departure_time": time(11, 30),
        "arrival_time": time(13, 30),
        "days_of_week": [1, 2, 3, 4, 5, 6, 7],
        "type_iata": "320",
        "effective_from": date(2025, 1, 1),
        "effective_until": None,
    },
    {
        "flight_number": "PK201",
        "airline_iata": "PK",
        "origin_iata": "LHE",
        "destination_iata": "ISB",
        "departure_time": time(7, 0),
        "arrival_time": time(7, 55),
        "days_of_week": [1, 2, 3, 4, 5],
        "type_iata": "738",
        "effective_from": date(2025, 1, 1),
        "effective_until": None,
    },
    {
        "flight_number": "PK711",
        "airline_iata": "PK",
        "origin_iata": "LHE",
        "destination_iata": "DXB",
        "departure_time": time(22, 0),
        "arrival_time": time(0, 30),
        "days_of_week": [1, 3, 5, 7],
        "type_iata": "738",
        "effective_from": date(2025, 3, 1),
        "effective_until": date(2025, 10, 25),
    },
    {
        "flight_number": "EK622",
        "airline_iata": "EK",
        "origin_iata": "DXB",
        "destination_iata": "LHE",
        "departure_time": time(9, 45),
        "arrival_time": time(14, 0),
        "days_of_week": [1, 2, 3, 4, 5, 6, 7],
        "type_iata": "77W",
        "effective_from": date(2025, 1, 1),
        "effective_until": None,
    },
    {
        "flight_number": "QR628",
        "airline_iata": "QR",
        "origin_iata": "DOH",
        "destination_iata": "ISB",
        "departure_time": time(2, 15),
        "arrival_time": time(7, 30),
        "days_of_week": [1, 3, 5, 6],
        "type_iata": "789",
        "effective_from": date(2025, 1, 1),
        "effective_until": None,
    },
    {
        "flight_number": "TK714",
        "airline_iata": "TK",
        "origin_iata": "IST",
        "destination_iata": "LHE",
        "departure_time": time(1, 30),
        "arrival_time": time(10, 15),
        "days_of_week": [2, 4, 6],
        "type_iata": "321",
        "effective_from": date(2025, 4, 1),
        "effective_until": None,
    },
    {
        "flight_number": "SV702",
        "airline_iata": "SV",
        "origin_iata": "JED",
        "destination_iata": "LHE",
        "departure_time": time(23, 0),
        "arrival_time": time(5, 0),
        "days_of_week": [1, 4, 7],
        "type_iata": "738",
        "effective_from": date(2025, 1, 15),
        "effective_until": None,
    },
]


def seed_scheduled_flights(db: Session) -> None:
    for data in SCHEDULED_FLIGHTS:
        airline = db.execute(
            select(Airline).where(Airline.iata_code == data["airline_iata"])
        ).scalar_one()
        origin = db.execute(
            select(Airport).where(Airport.iata_code == data["origin_iata"])
        ).scalar_one()
        destination = db.execute(
            select(Airport).where(Airport.iata_code == data["destination_iata"])
        ).scalar_one()
        aircraft_type = db.execute(
            select(AircraftType).where(AircraftType.iata_code == data["type_iata"])
        ).scalar_one()

        existing = db.execute(
            select(ScheduledFlight).where(
                ScheduledFlight.flight_number == data["flight_number"],
                ScheduledFlight.airline_id == airline.id,
                ScheduledFlight.effective_from == data["effective_from"],
            )
        ).scalar_one_or_none()
        if existing is not None:
            continue

        db.add(ScheduledFlight(
            flight_number=data["flight_number"],
            airline_id=airline.id,
            origin_id=origin.id,
            destination_id=destination.id,
            departure_time=data["departure_time"],
            arrival_time=data["arrival_time"],
            days_of_week=data["days_of_week"],
            aircraft_type_id=aircraft_type.id,
            effective_from=data["effective_from"],
            effective_until=data["effective_until"],
        ))
    db.commit()
