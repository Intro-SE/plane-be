from sqlalchemy import Column, String, Integer, CheckConstraint
from app.models.base import Base


class Rules(Base):
    __tablename__ = "rules"
    
    max_airports = Column(Integer,primary_key=True, default=10)
    max_transit_airports = Column(Integer, default=2)
    min_flight_time = Column(Integer, default=30)
    min_stop_time = Column(Integer, default=10)
    max_stop_time = Column(Integer, default=20)
    latest_booking_time = Column(Integer, default=1)
    latest_cancel_time = Column(Integer, default=1)
    ticket_class_count = Column(Integer, default=2)
    
    
    __table_args__ = (
        CheckConstraint("max_airports >= 0", name="check_max_airports"),
        CheckConstraint("max_transit_airports >= 0", name="check_max_transit_airports"),
        CheckConstraint("min_flight_time > 0", name="check_min_flight_time"),
        CheckConstraint("min_stop_time > 0", name="check_min_stop_time"),
        CheckConstraint("max_stop_time >= min_stop_time", name="check_max_stop_time"),
        CheckConstraint("latest_booking_time > 0", name="check_latest_booking_time"),
        CheckConstraint("latest_cancel_time > 0", name="check_latest_cancel_time"),
        CheckConstraint("ticket_class_count > 0", name="check_ticket_class_count"),
    )