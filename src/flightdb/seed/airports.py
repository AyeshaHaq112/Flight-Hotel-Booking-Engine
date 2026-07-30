from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from flightdb.models.geography import Airport

AIRPORTS = [
    {
        "iata_code": "LHE",
        "icao_code": "OPLA",
        "name": "Allama Iqbal International Airport",
        "city": "Lahore",
        "country": "PK",
        "latitude": Decimal("31.521564"),
        "longitude": Decimal("74.403594"),
        "elevation_ft": 712,
        "tz": "Asia/Karachi",
    },
    {
        "iata_code": "KHI",
        "icao_code": "OPKC",
        "name": "Jinnah International Airport",
        "city": "Karachi",
        "country": "PK",
        "latitude": Decimal("24.906500"),
        "longitude": Decimal("67.160500"),
        "elevation_ft": 100,
        "tz": "Asia/Karachi",
    },
    {
        "iata_code": "ISB",
        "icao_code": "OPIS",
        "name": "Islamabad International Airport",
        "city": "Islamabad",
        "country": "PK",
        "latitude": Decimal("33.549099"),
        "longitude": Decimal("72.824600"),
        "elevation_ft": 1665,
        "tz": "Asia/Karachi",
    },
    {
        "iata_code": "DXB",
        "icao_code": "OMDB",
        "name": "Dubai International Airport",
        "city": "Dubai",
        "country": "AE",
        "latitude": Decimal("25.252778"),
        "longitude": Decimal("55.364444"),
        "elevation_ft": 62,
        "tz": "Asia/Dubai",
    },
    {
        "iata_code": "DOH",
        "icao_code": "OTHH",
        "name": "Hamad International Airport",
        "city": "Doha",
        "country": "QA",
        "latitude": Decimal("25.273056"),
        "longitude": Decimal("51.608056"),
        "elevation_ft": 13,
        "tz": "Asia/Qatar",
    },
    {
        "iata_code": "JED",
        "icao_code": "OEJN",
        "name": "King Abdulaziz International Airport",
        "city": "Jeddah",
        "country": "SA",
        "latitude": Decimal("21.679564"),
        "longitude": Decimal("39.156536"),
        "elevation_ft": 48,
        "tz": "Asia/Riyadh",
    },
    {
        "iata_code": "IST",
        "icao_code": "LTFM",
        "name": "Istanbul Airport",
        "city": "Istanbul",
        "country": "TR",
        "latitude": Decimal("41.275278"),
        "longitude": Decimal("28.751944"),
        "elevation_ft": 325,
        "tz": "Europe/Istanbul",
    },
]


def seed_airports(db: Session) -> None:
    for data in AIRPORTS:
        existing = db.execute(
            select(Airport).where(Airport.iata_code == data["iata_code"])
        ).scalar_one_or_none()
        if existing is None:
            db.add(Airport(**data))
    db.commit()
