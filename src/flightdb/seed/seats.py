from sqlalchemy import select
from sqlalchemy.orm import Session

from flightdb.models.fleet import AircraftType, CabinLayout, Seat

SEAT_CONFIGS = [
    {
        "type_iata": "320",
        "layout_name": "standard",
        "columns": "ABCDEF",
        "sections": [
            {"cabin_class": "economy", "rows": range(1, 31), "exit_rows": {1, 12, 13}},
        ],
    },
    {
        "type_iata": "320",
        "layout_name": "two-class",
        "columns": "ABCDEF",
        "sections": [
            {"cabin_class": "business", "rows": range(1, 6), "exit_rows": {1}},
            {"cabin_class": "economy", "rows": range(6, 31), "exit_rows": {12, 13}},
        ],
    },
    {
        "type_iata": "738",
        "layout_name": "standard",
        "columns": "ABCDEF",
        "sections": [
            {"cabin_class": "economy", "rows": range(1, 32), "exit_rows": {1, 14, 15}},
        ],
    },
    {
        "type_iata": "738",
        "layout_name": "two-class",
        "columns": "ABCDEF",
        "sections": [
            {"cabin_class": "business", "rows": range(1, 5), "exit_rows": {1}},
            {"cabin_class": "economy", "rows": range(5, 32), "exit_rows": {14, 15}},
        ],
    },
    {
        "type_iata": "321",
        "layout_name": "standard",
        "columns": "ABCDEF",
        "sections": [
            {"cabin_class": "economy", "rows": range(1, 37), "exit_rows": {1, 16, 17}},
        ],
    },
    {
        "type_iata": "321",
        "layout_name": "two-class",
        "columns": "ABCDEF",
        "sections": [
            {"cabin_class": "business", "rows": range(1, 6), "exit_rows": {1}},
            {"cabin_class": "economy", "rows": range(6, 37), "exit_rows": {16, 17}},
        ],
    },
    {
        "type_iata": "77W",
        "layout_name": "three-class",
        "columns": "ABCDEFGHJ",
        "sections": [
            {"cabin_class": "first", "rows": range(1, 5), "exit_rows": {1}},
            {"cabin_class": "business", "rows": range(5, 15), "exit_rows": {5}},
            {"cabin_class": "economy", "rows": range(15, 50), "exit_rows": {15, 30}},
        ],
    },
    {
        "type_iata": "789",
        "layout_name": "two-class",
        "columns": "ABCDEFGHJ",
        "sections": [
            {"cabin_class": "business", "rows": range(1, 8), "exit_rows": {1}},
            {"cabin_class": "economy", "rows": range(8, 40), "exit_rows": {8, 25}},
        ],
    },
]


def _is_window(col: str, columns: str) -> bool:
    return col == columns[0] or col == columns[-1]


def _is_aisle(col: str, columns: str) -> bool:
    if len(columns) == 6:
        return col in ("C", "D")
    if len(columns) == 9:
        return col in ("C", "D", "F", "G")
    return False


def seed_seats(db: Session) -> None:
    for config in SEAT_CONFIGS:
        aircraft_type = db.execute(
            select(AircraftType).where(AircraftType.iata_code == config["type_iata"])
        ).scalar_one()

        cabin_layout = db.execute(
            select(CabinLayout).where(
                CabinLayout.aircraft_type_id == aircraft_type.id,
                CabinLayout.name == config["layout_name"],
            )
        ).scalar_one()

        existing_count = db.execute(
            select(Seat).where(Seat.cabin_layout_id == cabin_layout.id)
        ).first()
        if existing_count is not None:
            continue

        columns = config["columns"]
        for section in config["sections"]:
            for row_num in section["rows"]:
                for col in columns:
                    seat_no = f"{row_num}{col}"
                    db.add(Seat(
                        cabin_layout_id=cabin_layout.id,
                        seat_no=seat_no,
                        cabin_class=section["cabin_class"],
                        row_num=row_num,
                        column_letter=col,
                        is_window=_is_window(col, columns),
                        is_aisle=_is_aisle(col, columns),
                        is_exit_row=row_num in section["exit_rows"],
                    ))
    db.commit()
