from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class ThongKeHangVeChuyenBay(Base):
    __tablename__ = "thongkehangvechuyenbay"

    mathongkehangvecb = Column(String(50), primary_key=True)
    machuyenbay = Column(String(50), ForeignKey("chuyenbay.machuyenbay"), nullable=False)
    mahangve = Column(String(50), ForeignKey("hangve.mahangve"), nullable=False)
    soluongghe = Column(Integer, nullable=False)
    soghetrong = Column(Integer, nullable=False)
    soghedat = Column(Integer, nullable=False)

    # Relationships
    chuyenbay = relationship("ChuyenBay", back_populates="thongkehangves")
    hangve = relationship("HangVe", back_populates="thongkehangves") 