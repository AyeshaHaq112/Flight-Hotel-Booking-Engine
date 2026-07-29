from sqlalchemy import Boolean, Integer, Numeric, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flightdb.models.base import Base, TimestampMixin


class Airline(TimestampMixin, Base):
    __tablename__ = "airlines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    iata_code: Mapped[str] = mapped_column(String(2), unique=True, nullable=False)
    icao_code: Mapped[str | None] = mapped_column(String(3), unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(2), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, server_default="true", nullable=False)

    routes: Mapped[list["Route"]] = relationship(back_populates="airline")


class Airport(TimestampMixin, Base):
    __tablename__ = "airports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    iata_code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False)
    icao_code: Mapped[str | None] = mapped_column(String(4), unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(2), nullable=False)
    latitude: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)
    longitude: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)
    elevation_ft: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tz: Mapped[str] = mapped_column(String(50), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, server_default="true", nullable=False)


class Route(TimestampMixin, Base):
    __tablename__ = "routes"
    __table_args__ = (
        UniqueConstraint("airline_id", "origin_id", "destination_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    airline_id: Mapped[int] = mapped_column(ForeignKey("airlines.id"), nullable=False)
    origin_id: Mapped[int] = mapped_column(ForeignKey("airports.id"), nullable=False)
    destination_id: Mapped[int] = mapped_column(ForeignKey("airports.id"), nullable=False)
    distance_km: Mapped[int | None] = mapped_column(Integer, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, server_default="true", nullable=False)

    airline: Mapped["Airline"] = relationship(back_populates="routes")
    origin: Mapped["Airport"] = relationship(foreign_keys=[origin_id])
    destination: Mapped["Airport"] = relationship(foreign_keys=[destination_id])
