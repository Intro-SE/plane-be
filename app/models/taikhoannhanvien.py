from sqlalchemy import Column, String, Date, CheckConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base

class TaiKhoanNhanVien(Base):
    __tablename__ = "TAIKHOANNHANVIEN"

    IDNHANVIEN = Column(String(50), primary_key=True)
    TENDANGNHAP = Column(String(200), nullable=False)
    MATKHAU = Column(String(200), nullable=False)
    TENNHANVIEN = Column(String(50), nullable=False)
    CMND_CCCD = Column(String(50), nullable=False)
    SODIENTHOAI = Column(String(50), nullable=False)
    GIOITINH = Column(String(3))
    NGAYTHEM = Column(Date, nullable=False)

    # Relationships
    phieudatchos = relationship("PhieuDatChoVeMayBay", back_populates="nhanvien")

    __table_args__ = (
        CheckConstraint("GIOITINH IN ('Nam', 'Nữ')"),
    ) 