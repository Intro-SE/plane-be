from sqlalchemy import Column, String, Date, Boolean, BigInteger, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, joinedload
from app.models.base import Base

class PhieuDatChoVeMayBay(Base):
    __tablename__ = "phieudatcho_vemaybay"

    maphieudatcho = Column(String(50), primary_key=True)
    machuyenbay = Column(String(50), ForeignKey("chuyenbay.machuyenbay"), nullable=False)
    tenhanhkhach = Column(String(50), nullable=False)
    cmnd_cccd = Column(String(12), nullable=False)
    gioitinh = Column(String(3))
    sodienthoai = Column(String(12), nullable=False)
    mahangve = Column(String(50), ForeignKey("hangve.mahangve"), nullable=False)
    giatien = Column(BigInteger, nullable=False)
    ngaydat = Column(Date, nullable=False)
    trangthailayve = Column(Boolean, nullable=False)
    idnhanvien = Column(String(50), ForeignKey("taikhoannhanvien.idnhanvien"), nullable=False)

    # Relationships
    chuyenbay = relationship("ChuyenBay", back_populates="phieudatchos", lazy="joined")
    hangve = relationship("HangVe", back_populates="phieudatchos", lazy="joined")
    nhanvien = relationship("TaiKhoanNhanVien", back_populates="phieudatchos", lazy="joined")

    __table_args__ = (
        CheckConstraint("gioitinh IN ('Nam', 'Nữ')"),
    ) 