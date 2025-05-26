from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class DonGia(Base):
    __tablename__ = "DONGIA"

    MADONGIA = Column(String(50), primary_key=True)
    MATUYENBAY = Column(String(50), ForeignKey("TUYENBAY.MATUYENBAY"), nullable=False)
    MAHANGVE = Column(String(50), ForeignKey("HANGVE.MAHANGVE"), nullable=False)
    GIATIEN = Column(Integer, nullable=False)

    # Relationships
    tuyenbay = relationship("TuyenBay", back_populates="dongias")
    hangve = relationship("HangVe", back_populates="dongias") 