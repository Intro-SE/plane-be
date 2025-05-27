from sqlalchemy import Column, String, Date, Time, Integer, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from app.models.base import Base

class ChuyenBay(Base):
    __tablename__ = "chuyenbay"

    machuyenbay = Column(String(50), primary_key=True)
    matuyenbay = Column(String(50), ForeignKey("tuyenbay.matuyenbay"), nullable=False)
    ngaybay = Column(Date, nullable=False)
    giobay = Column(Time, nullable=False)
    thoigianbay = Column(Integer, nullable=False)
    soghechuyenbay = Column(Integer, nullable=False)

    # Relationships
    tuyenbay = relationship("TuyenBay", back_populates="chuyenbays", lazy="joined")
    thongkehangves = relationship("ThongKeHangVeChuyenBay", back_populates="chuyenbay", lazy="joined")
    phieudatchos = relationship("PhieuDatChoVeMayBay", back_populates="chuyenbay", lazy="joined") 