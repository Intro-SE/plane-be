from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class HangVe(Base):
    __tablename__ = "HANGVE"

    MAHANGVE = Column(String(50), primary_key=True)
    TENHANGVE = Column(String(50), nullable=False)

    # Relationships
    thongkehangves = relationship("ThongKeHangVeChuyenBay", back_populates="hangve")
    dongias = relationship("DonGia", back_populates="hangve")
    phieudatchos = relationship("PhieuDatChoVeMayBay", back_populates="hangve") 