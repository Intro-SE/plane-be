from sqlalchemy import Column, String, Date, CheckConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base

class Employee(Base):
    __tablename__ = "employee"

    employee_id = Column(String(50), primary_key=True)
    employee_username = Column(String(200), nullable=False)
    employee_password = Column(String(200), nullable=False)
    employee_name = Column(String(50), nullable=False)
    national_id = Column(String(50), nullable=False)
    gender = Column(String(3), nullable=True)
    phone_number = Column(String(50), nullable=False)
    created_date = Column(Date, nullable=False)

    # Relationships
    booking_tickets = relationship("BookingTicket", back_populates="employee", lazy="joined")

    __table_args__ = (
        CheckConstraint("gender IN ('Nam', 'Nữ')", name="ck_employee_gender"),
    )
