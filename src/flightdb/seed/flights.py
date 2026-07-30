from datetime import date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from flightdb.models.fleet import Aircraft, CabinLayout
from flightdb.models.geography import Airline, Airport
from flightdb.models.schedule import Flight, ScheduledFlight


FLIGHTS_DATA = [
    {
        "flight_number": "PK301",
        "airline_iata": "PK",
        "origin_iata": "LHE",
        "destination_iata": "KHI",
        "service_date": date(2025, 8, 4),
        "status": "scheduled",
    },
    {
        "flight_number": "PK301",
        "airline_iata": "PK",
        "origin_iata": "LHE",
        "destination_iata": "KHI",
        "service_date": date(2025, 8, 5),
        "status": "scheduled",
    },
    {
        "flight_number": "PK302",
        "airline_iata": "PK",
        "origin_iata": "KHI",
        "destination_iata": "LHE",
        "service_date": date(2025, 8, 4),
        "status": "scheduled",
    },
    {
        "flight_number": "PK201",
        "airline_iata": "PK",
        "origin_iata": "LHE",
        "destination_iata": "ISB",
        "service_date": date(2025, 8, 4),
        "status": "scheduled",
    },
    {
        "flight_number": "EK622",
        "airline_iata": "EK",
        "origin_iata": "DXB",
        "destination_iata": "LHE",
        "service_date": date(2025, 8, 4),
        "status": "scheduled",
    },
    {
        "flight_number": "EK622",
        "airline_iata": "EK",
        "origin_iata": "DXB",
        "destination_iata": "LHE",
        "service_date": date(2025, 8, 5),
        "status": "scheduled",
    },
    {
        "flight_number": "QR628",
        "airline_iata": "QR",
        "origin_iata": "DOH",
        "destination_iata": "ISB",
        "service_date": date(2025, 8, 4),
        "status": "scheduled",
    },
    {
        "flight_number": "TK714",
        "airline_iata": "TK",
        "origin_iata": "IST",
        "destination_iata": "LHE",
        "service_date": date(2025, 8, 5),
        "status": "scheduled",
    },
]


def _make_departure_utc(
    service_date: date, departure_time, origin_tz_name: str
) -> datetime:
    tz = ZoneInfo(origin_tz_name)
    local_dt = datetime.combine(service_date, departure_time, tzinfo=tz)
    return local_dt


def _make_arrival_utc(
    departure_dt: datetime, departure_time, arrival_time
) -> datetime:
    dep_minutes = departure_time.hour * 60 + departure_time.minute
    arr_minutes = arrival_time.hour * 60 + arrival_time.minute

    if arr_minutes > dep_minutes:
        duration = timedelta(minutes=arr_minutes - dep_minutes)
    else:
        duration = timedelta(minutes=(1440 - dep_minutes) + arr_minutes)

    return departure_dt + duration


def seed_flights(db: Session) -> None:
    for data in FLIGHTS_DATA:
        airline = db.execute(
            select(Airline).where(Airline.iata_code == data["airline_iata"])
        ).scalar_one()
        origin = db.execute(
            select(Airport).where(Airport.iata_code == data["origin_iata"])
        ).scalar_one()
        destination = db.execute(
            select(Airport).where(Airport.iata_code == data["destination_iata"])
        ).scalar_one()

        scheduled_flight = db.execute(
            select(ScheduledFlight).where(
                ScheduledFlight.flight_number == data["flight_number"],
                ScheduledFlight.airline_id == airline.id,
                ScheduledFlight.origin_id == origin.id,
                ScheduledFlight.destination_id == destination.id,
            )
        ).scalar_one()

        existing = db.execute(
            select(Flight).where(
                Flight.scheduled_flight_id == scheduled_flight.id,
                Flight.service_date == data["service_date"],
            )
        ).scalar_one_or_none()
        if existing is not None:
            continue

        aircraft = db.execute(
            select(Aircraft).where(
                Aircraft.airline_id == airline.id,
                Aircraft.aircraft_type_id == scheduled_flight.aircraft_type_id,
            )
        ).first()

        cabin_layout = None
        aircraft_obj = None
        if aircraft is not None:
            aircraft_obj = aircraft[0]
            cabin_layout = db.execute(
                select(CabinLayout).where(
                    CabinLayout.aircraft_type_id == scheduled_flight.aircraft_type_id,
                    CabinLayout.name == "standard",
                )
            ).scalar_one_or_none()

        departure_dt = _make_departure_utc(
            data["service_date"],
            scheduled_flight.departure_time,
            origin.tz,
        )
        arrival_dt = _make_arrival_utc(
            departure_dt,
            scheduled_flight.departure_time,
            scheduled_flight.arrival_time,
        )

        db.add(Flight(
            scheduled_flight_id=scheduled_flight.id,
            flight_number=data["flight_number"],
            service_date=data["service_date"],
            aircraft_id=aircraft_obj.id if aircraft_obj else None,
            cabin_layout_id=cabin_layout.id if cabin_layout else None,
            departure_scheduled=departure_dt,
            arrival_scheduled=arrival_dt,
            departure_actual=None,
            arrival_actual=None,
            status=data["status"],
        ))
    db.commit()
