from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class ChiTietChuyenBay(Base):
    __tablename__ = "CHITIETCHUYENBAY"

    MACHITIETCHUYENBAY = Column(String(50), primary_key=True)
    MATUYENBAY = Column(String(50), ForeignKey("TUYENBAY.MATUYENBAY"), nullable=False)
    MASANBAYTRUNGGIAN = Column(String(50), ForeignKey("SANBAY.MASANBAY"), nullable=False)
    THOIGIANDUNG = Column(Integer, nullable=False)
    GHICHU = Column(String(200))

    # Relationships
    tuyenbay = relationship("TuyenBay", back_populates="chitietchuyenbays")
    sanbaytrunggian = relationship("SanBay") 