from sqlalchemy import Column, String, Date, Boolean, BigInteger, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base

class PhieuDatChoVeMayBay(Base):
    __tablename__ = "PHIEUDATCHO_VEMAYBAY"

    MAPHIEUDATCHO = Column(String(50), primary_key=True)
    MACHUYENBAY = Column(String(50), ForeignKey("CHUYENBAY.MACHUYENBAY"), nullable=False)
    TENHANHKHACH = Column(String(50), nullable=False)
    CMND_CCCD = Column(String(50), nullable=False)
    GIOITINH = Column(String(3))
    SODIENTHOAI = Column(String(12), nullable=False)
    MAHANGVE = Column(String(50), ForeignKey("HANGVE.MAHANGVE"), nullable=False)
    GIATIEN = Column(BigInteger, nullable=False)
    NGAYDAT = Column(Date, nullable=False)
    TRANGTHAILAYVE = Column(Boolean, nullable=False)
    IDNHANVIEN = Column(String(50), ForeignKey("TAIKHOANNHANVIEN.IDNHANVIEN"), nullable=False)

    # Relationships
    chuyenbay = relationship("ChuyenBay", back_populates="phieudatchos")
    hangve = relationship("HangVe", back_populates="phieudatchos")
    nhanvien = relationship("TaiKhoanNhanVien", back_populates="phieudatchos")

    __table_args__ = (
        CheckConstraint("GIOITINH IN ('Nam', 'Nữ')"),
    ) 