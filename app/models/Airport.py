from sqlalchemy import Column, String
from app.models.base import Base

class Airport(Base):
    __tablename__ = "airport"

    airport_id = Column(String(50), primary_key=True)
    airport_name = Column(String(50), nullable=False)
    airport_address = Column(String(50), nullable=False)