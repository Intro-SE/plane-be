from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, joinedload
from app.models.base import Base

class HangVe(Base):
    __tablename__ = "hangve"

    mahangve = Column(String(50), primary_key=True)
    tenhangve = Column(String(50), nullable=False)

    # Relationships
    thongkehangves = relationship("ThongKeHangVeChuyenBay", back_populates="hangve", lazy="joined")
    dongias = relationship("DonGia", back_populates="hangve", lazy="joined")
    phieudatchos = relationship("PhieuDatChoVeMayBay", back_populates="hangve", lazy="joined") 