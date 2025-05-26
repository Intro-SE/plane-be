from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .chuyenbay import ChuyenBayInDB
from .hangve import HangVeInDB
from .taikhoannhanvien import TaiKhoanNhanVienInDB

class PhieuDatChoVeMayBayBase(BaseModel):
    MAPHIEUDATCHO: str
    MACHUYENBAY: str
    TENHANHKHACH: str = Field(..., min_length=1, max_length=50)
    CMND_CCCD: str = Field(..., pattern=r'^\d{9}|\d{12}$')
    GIOITINH: str = Field(..., pattern=r'^(Nam|Nữ)$')
    SODIENTHOAI: str = Field(..., pattern=r'^\d{10}$')
    MAHANGVE: str
    GIATIEN: int = Field(..., gt=0)
    NGAYDAT: datetime
    TRANGTHAILAYVE: bool
    IDNHANVIEN: str

    class Config:
        from_attributes = True

class PhieuDatChoVeMayBayCreate(BaseModel):
    MACHUYENBAY: str
    TENHANHKHACH: str = Field(..., min_length=1, max_length=50)
    CMND_CCCD: str = Field(..., pattern=r'^\d{9}|\d{12}$')
    GIOITINH: str = Field(..., pattern=r'^(Nam|Nữ)$')
    SODIENTHOAI: str = Field(..., pattern=r'^\d{10}$')
    MAHANGVE: str
    GIATIEN: int = Field(..., gt=0)
    TRANGTHAILAYVE: bool = Field(default=False)
    IDNHANVIEN: str

    class Config:
        from_attributes = True

class PhieuDatChoVeMayBayUpdate(BaseModel):
    TENHANHKHACH: str | None = Field(None, min_length=1, max_length=50)
    CMND_CCCD: str | None = Field(None, pattern=r'^\d{9}|\d{12}$')
    GIOITINH: str | None = Field(None, pattern=r'^(Nam|Nữ)$')
    SODIENTHOAI: str | None = Field(None, pattern=r'^\d{10}$')
    MAHANGVE: str | None = None
    GIATIEN: int | None = Field(None, gt=0)
    TRANGTHAILAYVE: bool | None = None

    class Config:
        from_attributes = True

class PhieuDatChoVeMayBayInDB(PhieuDatChoVeMayBayBase):
    chuyenbay: ChuyenBayInDB
    hangve: HangVeInDB
    nhanvien: TaiKhoanNhanVienInDB

    @property
    def trang_thai_ve(self) -> str:
        return "Đã lấy vé" if self.TRANGTHAILAYVE else "Chưa lấy vé"

    @property
    def ngay_dat_format(self) -> str:
        return self.NGAYDAT.strftime("%d/%m/%Y %H:%M")

    @property
    def gia_tien_format(self) -> str:
        return f"{self.GIATIEN:,} VNĐ"

    class Config:
        from_attributes = True 