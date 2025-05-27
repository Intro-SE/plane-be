from sqlalchemy import Column, String, Date, CheckConstraint
from sqlalchemy.orm import relationship, joinedload
from app.models.base import Base

class TaiKhoanNhanVien(Base):
    __tablename__ = "taikhoannhanvien"

    idnhanvien = Column(String(50), primary_key=True)
    tendangnhap = Column(String(200), nullable=False)
    matkhau = Column(String(200), nullable=False)
    tennhanvien = Column(String(50), nullable=False)
    cmnd_cccd = Column(String(50), nullable=False)
    sodienthoai = Column(String(50), nullable=False)
    gioitinh = Column(String(3))
    ngaythem = Column(Date, nullable=False)

    # Relationships
    phieudatchos = relationship("PhieuDatChoVeMayBay", back_populates="nhanvien", lazy="joined")

    __table_args__ = (
        CheckConstraint("gioitinh IN ('Nam', 'Nữ')"),
    ) 