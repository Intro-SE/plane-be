from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class ThongKeHangVeChuyenBay(Base):
    __tablename__ = "THONGKEHANGVECHUYENBAY"

    MATHONGKEHANGVECB = Column(String(50), primary_key=True)
    MACHUYENBAY = Column(String(50), ForeignKey("CHUYENBAY.MACHUYENBAY"), nullable=False)
    MAHANGVE = Column(String(50), ForeignKey("HANGVE.MAHANGVE"), nullable=False)
    SOLUONGGHE = Column(Integer, nullable=False)
    SOGHETRONG = Column(Integer, nullable=False)
    SOGHEDAT = Column(Integer, nullable=False)

    # Relationships
    chuyenbay = relationship("ChuyenBay", back_populates="thongkehangves")
    hangve = relationship("HangVe", back_populates="thongkehangves") 