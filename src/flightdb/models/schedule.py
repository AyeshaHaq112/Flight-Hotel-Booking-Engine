from __future__ import annotations

from datetime import date, datetime, time
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Integer,
    String,
    Time,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flightdb.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from flightdb.models.fleet import Aircraft, CabinLayout, AircraftType
    from flightdb.models.geography import Airline, Airport


class ScheduledFlight(TimestampMixin, Base):
    __tablename__ = "scheduled_flights"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    flight_number: Mapped[str] = mapped_column(String(6), nullable=False)
    airline_id: Mapped[int] = mapped_column(ForeignKey("airlines.id"), nullable=False)
    origin_id: Mapped[int] = mapped_column(ForeignKey("airports.id"), nullable=False)
    destination_id: Mapped[int] = mapped_column(ForeignKey("airports.id"), nullable=False)
    departure_time: Mapped[time] = mapped_column(Time, nullable=False)
    arrival_time: Mapped[time] = mapped_column(Time, nullable=False)
    days_of_week: Mapped[list[int]] = mapped_column(
        ARRAY(Integer), nullable=False
    )
    aircraft_type_id: Mapped[int] = mapped_column(
        ForeignKey("aircraft_types.id"), nullable=False
    )
    effective_from: Mapped[date] = mapped_column(Date, nullable=False)
    effective_until: Mapped[date | None] = mapped_column(Date, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, server_default="true", nullable=False)

    airline: Mapped["Airline"] = relationship()
    origin: Mapped["Airport"] = relationship(foreign_keys=[origin_id])
    destination: Mapped["Airport"] = relationship(foreign_keys=[destination_id])
    aircraft_type: Mapped["AircraftType"] = relationship()
    flights: Mapped[list["Flight"]] = relationship(back_populates="scheduled_flight")


class Flight(TimestampMixin, Base):
    __tablename__ = "flights"
    __table_args__ = (
        UniqueConstraint("scheduled_flight_id", "service_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scheduled_flight_id: Mapped[int] = mapped_column(
        ForeignKey("scheduled_flights.id"), nullable=False
    )
    flight_number: Mapped[str] = mapped_column(String(6), nullable=False)
    service_date: Mapped[date] = mapped_column(Date, nullable=False)
    aircraft_id: Mapped[int | None] = mapped_column(
        ForeignKey("aircraft.id"), nullable=True
    )
    cabin_layout_id: Mapped[int | None] = mapped_column(
        ForeignKey("cabin_layouts.id"), nullable=True
    )
    departure_scheduled: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    arrival_scheduled: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    departure_actual: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    arrival_actual: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(20), server_default="scheduled", nullable=False
    )

    scheduled_flight: Mapped["ScheduledFlight"] = relationship(back_populates="flights")
    aircraft: Mapped["Aircraft | None"] = relationship()
    cabin_layout: Mapped["CabinLayout | None"] = relationship()
