from sqlalchemy import select
from sqlalchemy.orm import Session

from flightdb.models.geography import Airline, Airport, Route

ROUTES = [
    {"airline_iata": "PK", "origin_iata": "LHE", "destination_iata": "KHI", "distance_km": 1024},
    {"airline_iata": "PK", "origin_iata": "KHI", "destination_iata": "LHE", "distance_km": 1024},
    {"airline_iata": "PK", "origin_iata": "LHE", "destination_iata": "ISB", "distance_km": 286},
    {"airline_iata": "PK", "origin_iata": "ISB", "destination_iata": "LHE", "distance_km": 286},
    {"airline_iata": "PK", "origin_iata": "LHE", "destination_iata": "DXB", "distance_km": 1918},
    {"airline_iata": "PK", "origin_iata": "ISB", "destination_iata": "JED", "distance_km": 2973},
    {"airline_iata": "EK", "origin_iata": "DXB", "destination_iata": "LHE", "distance_km": 1918},
    {"airline_iata": "EK", "origin_iata": "DXB", "destination_iata": "KHI", "distance_km": 1228},
    {"airline_iata": "EK", "origin_iata": "DXB", "destination_iata": "ISB", "distance_km": 2012},
    {"airline_iata": "QR", "origin_iata": "DOH", "destination_iata": "ISB", "distance_km": 2277},
    {"airline_iata": "QR", "origin_iata": "DOH", "destination_iata": "LHE", "distance_km": 2453},
    {"airline_iata": "TK", "origin_iata": "IST", "destination_iata": "LHE", "distance_km": 4243},
    {"airline_iata": "TK", "origin_iata": "IST", "destination_iata": "ISB", "distance_km": 4019},
    {"airline_iata": "SV", "origin_iata": "JED", "destination_iata": "LHE", "distance_km": 3248},
]


def seed_routes(db: Session) -> None:
    for data in ROUTES:
        airline = db.execute(
            select(Airline).where(Airline.iata_code == data["airline_iata"])
        ).scalar_one()
        origin = db.execute(
            select(Airport).where(Airport.iata_code == data["origin_iata"])
        ).scalar_one()
        destination = db.execute(
            select(Airport).where(Airport.iata_code == data["destination_iata"])
        ).scalar_one()

        existing = db.execute(
            select(Route).where(
                Route.airline_id == airline.id,
                Route.origin_id == origin.id,
                Route.destination_id == destination.id,
            )
        ).scalar_one_or_none()
        if existing is not None:
            continue

        db.add(Route(
            airline_id=airline.id,
            origin_id=origin.id,
            destination_id=destination.id,
            distance_km=data["distance_km"],
        ))
    db.commit()
