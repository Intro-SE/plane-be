from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class DonGia(Base):
    __tablename__ = "dongia"

    madongia = Column(String(50), primary_key=True)
    matuyenbay = Column(String(50), ForeignKey("tuyenbay.matuyenbay"), nullable=False)
    mahangve = Column(String(50), ForeignKey("hangve.mahangve"), nullable=False)
    giatien = Column(Integer, nullable=False)

    # Relationships
    tuyenbay = relationship("TuyenBay", back_populates="dongias")
    hangve = relationship("HangVe", back_populates="dongias") 