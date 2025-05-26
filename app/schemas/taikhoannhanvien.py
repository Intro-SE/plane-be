from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List, Optional
from .phieudatcho_vemaybay import PhieuDatChoVeMayBayInDB

class TaiKhoanNhanVienBase(BaseModel):
    IDNHANVIEN: str
    TENDANGNHAP: str = Field(..., min_length=3, max_length=200)
    MATKHAU: str = Field(..., min_length=6, max_length=200)
    TENNHANVIEN: str = Field(..., min_length=1, max_length=50)
    CMND_CCCD: str = Field(..., pattern=r'^\d{9}|\d{12}$')
    SODIENTHOAI: str = Field(..., pattern=r'^\d{10}$')
    GIOITINH: str | None = Field(None, pattern=r'^(Nam|Nữ)$')
    NGAYTHEM: datetime

    class Config:
        from_attributes = True

class TaiKhoanNhanVienCreate(BaseModel):
    TENDANGNHAP: str = Field(..., min_length=3, max_length=200)
    MATKHAU: str = Field(..., min_length=6, max_length=200)
    TENNHANVIEN: str = Field(..., min_length=1, max_length=50)
    CMND_CCCD: str = Field(..., pattern=r'^\d{9}|\d{12}$')
    SODIENTHOAI: str = Field(..., pattern=r'^\d{10}$')
    GIOITINH: str | None = Field(None, pattern=r'^(Nam|Nữ)$')
    NGAYTHEM: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True

class TaiKhoanNhanVienUpdate(BaseModel):
    TENDANGNHAP: str | None = Field(None, min_length=3, max_length=200)
    MATKHAU: str | None = Field(None, min_length=6, max_length=200)
    TENNHANVIEN: str | None = Field(None, min_length=1, max_length=50)
    CMND_CCCD: str | None = Field(None, pattern=r'^\d{9}|\d{12}$')
    SODIENTHOAI: str | None = Field(None, pattern=r'^\d{10}$')
    GIOITINH: str | None = Field(None, pattern=r'^(Nam|Nữ)$')

    class Config:
        from_attributes = True

class TaiKhoanNhanVienInDB(TaiKhoanNhanVienBase):
    phieudatchos: List[PhieuDatChoVeMayBayInDB] = []

    @property
    def so_phieu_dat(self) -> int:
        return len(self.phieudatchos)

    @property
    def ngay_them_format(self) -> str:
        return self.NGAYTHEM.strftime("%d/%m/%Y %H:%M")

    @property
    def trang_thai_hoat_dong(self) -> str:
        return "Đang hoạt động" if self.so_phieu_dat > 0 else "Chưa hoạt động"

    class Config:
        from_attributes = True 