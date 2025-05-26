from sqlalchemy import Column, String, Date, Time, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class ChuyenBay(Base):
    __tablename__ = "CHUYENBAY"

    MACHUYENBAY = Column(String(50), primary_key=True)
    MATUYENBAY = Column(String(50), ForeignKey("TUYENBAY.MATUYENBAY"), nullable=False)
    NGAYBAY = Column(Date, nullable=False)
    GIOBAY = Column(Time, nullable=False)
    THOIGIANBAY = Column(Integer, nullable=False)
    SOGHECHUYENBAY = Column(Integer, nullable=False)

    # Relationships
    tuyenbay = relationship("TuyenBay", back_populates="chuyenbays")
    thongkehangves = relationship("ThongKeHangVeChuyenBay", back_populates="chuyenbay")
    phieudatchos = relationship("PhieuDatChoVeMayBay", back_populates="chuyenbay") 