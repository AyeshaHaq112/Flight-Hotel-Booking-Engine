from flightdb.db import SessionLocal
from flightdb.seed.airlines import seed_airlines
from flightdb.seed.airports import seed_airports
from flightdb.seed.aircraft_types import seed_aircraft_types
from flightdb.seed.aircraft import seed_aircraft
from flightdb.seed.cabin_layouts import seed_cabin_layouts
from flightdb.seed.seats import seed_seats
from flightdb.seed.routes import seed_routes
from flightdb.seed.scheduled_flights import seed_scheduled_flights
from flightdb.seed.flights import seed_flights


def main() -> None:
    db = SessionLocal()
    try:
        print("Seeding airlines...")
        seed_airlines(db)

        print("Seeding airports...")
        seed_airports(db)

        print("Seeding aircraft types...")
        seed_aircraft_types(db)

        print("Seeding aircraft...")
        seed_aircraft(db)

        print("Seeding cabin layouts...")
        seed_cabin_layouts(db)

        print("Seeding seats...")
        seed_seats(db)

        print("Seeding routes...")
        seed_routes(db)

        print("Seeding scheduled flights...")
        seed_scheduled_flights(db)

        print("Seeding flights...")
        seed_flights(db)

        print("Done! All seed data inserted.")
    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
