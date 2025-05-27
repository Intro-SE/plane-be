from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class TuyenBay(Base):
    __tablename__ = "tuyenbay"

    matuyenbay = Column(String(50), primary_key=True)
    sanbaydi = Column(String(50), ForeignKey("sanbay.masanbay"), nullable=False)
    sanbayden = Column(String(50), ForeignKey("sanbay.masanbay"), nullable=False)

    # Relationships
    sanbay_di = relationship("SanBay", foreign_keys=[sanbaydi])
    sanbay_den = relationship("SanBay", foreign_keys=[sanbayden])
    chuyenbays = relationship("ChuyenBay", back_populates="tuyenbay")
    chitietchuyenbays = relationship("ChiTietChuyenBay", back_populates="tuyenbay")
    dongias = relationship("DonGia", back_populates="tuyenbay") 