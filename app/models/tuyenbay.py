from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class TuyenBay(Base):
    __tablename__ = "TUYENBAY"

    MATUYENBAY = Column(String(50), primary_key=True)
    SANBAYDI = Column(String(50), ForeignKey("SANBAY.MASANBAY"), nullable=False)
    SANBAYDEN = Column(String(50), ForeignKey("SANBAY.MASANBAY"), nullable=False)

    # Relationships
    sanbay_di = relationship("SanBay", foreign_keys=[SANBAYDI])
    sanbay_den = relationship("SanBay", foreign_keys=[SANBAYDEN])
    chuyenbays = relationship("ChuyenBay", back_populates="tuyenbay")
    chitietchuyenbays = relationship("ChiTietChuyenBay", back_populates="tuyenbay")
    dongias = relationship("DonGia", back_populates="tuyenbay") 