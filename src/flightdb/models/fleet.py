from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flightdb.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from flightdb.models.geography import Airline


class AircraftType(TimestampMixin, Base):
    __tablename__ = "aircraft_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    iata_code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    max_range_km: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cruise_speed_kmh: Mapped[int | None] = mapped_column(Integer, nullable=True)
  
    cabin_layouts: Mapped[list["CabinLayout"]] = relationship(back_populates="aircraft_type")
    aircraft: Mapped[list["Aircraft"]] = relationship(back_populates="aircraft_type")


class Aircraft(TimestampMixin, Base):
    __tablename__ = "aircraft"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    registration: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    aircraft_type_id: Mapped[int] = mapped_column(
        ForeignKey("aircraft_types.id"), nullable=False
    )
    airline_id: Mapped[int] = mapped_column(ForeignKey("airlines.id"), nullable=False)
    delivery_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), server_default="active", nullable=False
    )

    aircraft_type: Mapped["AircraftType"] = relationship(back_populates="aircraft")
    airline: Mapped["Airline"] = relationship()


class CabinLayout(TimestampMixin, Base):
    __tablename__ = "cabin_layouts"
    __table_args__ = (
        UniqueConstraint("aircraft_type_id", "name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    aircraft_type_id: Mapped[int] = mapped_column(
        ForeignKey("aircraft_types.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    total_seats: Mapped[int] = mapped_column(Integer, nullable=False)

    aircraft_type: Mapped["AircraftType"] = relationship(back_populates="cabin_layouts")
    seats: Mapped[list["Seat"]] = relationship(back_populates="cabin_layout")


class Seat(TimestampMixin, Base):
    __tablename__ = "seats"
    __table_args__ = (
        UniqueConstraint("cabin_layout_id", "seat_no"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cabin_layout_id: Mapped[int] = mapped_column(
        ForeignKey("cabin_layouts.id"), nullable=False
    )
    seat_no: Mapped[str] = mapped_column(String(4), nullable=False)
    cabin_class: Mapped[str] = mapped_column(String(10), nullable=False)
    row_num: Mapped[int] = mapped_column(Integer, nullable=False)
    column_letter: Mapped[str] = mapped_column(String(1), nullable=False)
    is_window: Mapped[bool] = mapped_column(Boolean, server_default="false", nullable=False)
    is_aisle: Mapped[bool] = mapped_column(Boolean, server_default="false", nullable=False)
    is_exit_row: Mapped[bool] = mapped_column(Boolean, server_default="false", nullable=False)

    cabin_layout: Mapped["CabinLayout"] = relationship(back_populates="seats")
