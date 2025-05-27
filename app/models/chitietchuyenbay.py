from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class ChiTietChuyenBay(Base):
    __tablename__ = "chitietchuyenbay"

    machitietchuyenbay = Column(String(50), primary_key=True)
    matuyenbay = Column(String(50), ForeignKey("tuyenbay.matuyenbay"), nullable=False)
    masanbaytrunggian = Column(String(50), ForeignKey("sanbay.masanbay"), nullable=False)
    thoigiandung = Column(Integer, nullable=False)
    ghichu = Column(String(200))

    # Relationships
    tuyenbay = relationship("TuyenBay", back_populates="chitietchuyenbays")
    sanbaytrunggian = relationship("SanBay") 