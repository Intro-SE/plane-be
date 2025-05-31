from sqlalchemy import Column, String, Date, Boolean, BigInteger, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base

class BookingTicket(Base):
    __tablename__ = "booking_ticket"

    booking_ticket_id = Column(String(50), primary_key=True)
    flight_id = Column(String(50), ForeignKey("flight.flight_id"), nullable=False)

    # Passenger Info
    passenger_name = Column(String(50), nullable=False)
    national_id = Column(String(50), nullable=False)
    gender = Column(String(3))
    phone_number = Column(String(12), nullable=False)

    # Ticket Info
    ticket_class_id = Column(String(50), ForeignKey("ticketclass.ticket_class_id"), nullable=False)
    booking_price = Column(BigInteger, nullable=False)
    booking_date = Column(Date, nullable=False)
    ticket_status = Column(Boolean, nullable=False)  # True: ticket, False: booking only

    # Employee Info
    employee_id = Column(String(50), ForeignKey("employee.employee_id"), nullable=False)

    # Relationships
    flight = relationship("Flight", back_populates="booking_tickets", lazy="joined")
    ticket_class = relationship("TicketClass", back_populates="booking_tickets", lazy="joined")
    employee = relationship("Employee", back_populates="booking_tickets", lazy="joined")

    __table_args__ = (
        CheckConstraint("gender IN ('Nam', 'Nữ')", name="ck_bookingticket_gender"),
    )