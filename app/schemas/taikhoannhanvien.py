from __future__ import annotations
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from app.schemas.phieudatcho_vemaybay import PhieuDatChoVeMayBayInDB

class TaiKhoanNhanVienBase(BaseModel):
    idnhanvien: str
    tendangnhap: str = Field(..., min_length=3, max_length=200)
    matkhau: str = Field(..., min_length=6, max_length=200)
    tennhanvien: str = Field(..., min_length=1, max_length=50)
    cmnd_cccd: str = Field(..., pattern=r'^\d{9}|\d{12}$')
    sodienthoai: str = Field(..., pattern=r'^\d{10}$')
    gioitinh: str | None = Field(None, pattern=r'^(Nam|Nữ)$')
    ngaythem: datetime

    class Config:
        from_attributes = True

class TaiKhoanNhanVienCreate(BaseModel):
    tendangnhap: str = Field(..., min_length=3, max_length=200)
    matkhau: str = Field(..., min_length=6, max_length=200)
    tennhanvien: str = Field(..., min_length=1, max_length=50)
    cmnd_cccd: str = Field(..., pattern=r'^\d{9}|\d{12}$')
    sodienthoai: str = Field(..., pattern=r'^\d{10}$')
    gioitinh: str | None = Field(None, pattern=r'^(Nam|Nữ)$')
    ngaythem: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True

class TaiKhoanNhanVienUpdate(BaseModel):
    tendangnhap: str | None = Field(None, min_length=3, max_length=200)
    matkhau: str | None = Field(None, min_length=6, max_length=200)
    tennhanvien: str | None = Field(None, min_length=1, max_length=50)
    cmnd_cccd: str | None = Field(None, pattern=r'^\d{9}|\d{12}$')
    sodienthoai: str | None = Field(None, pattern=r'^\d{10}$')
    gioitinh: str | None = Field(None, pattern=r'^(Nam|Nữ)$')

    class Config:
        from_attributes = True


class TaiKhoanNhanVienInDB(TaiKhoanNhanVienBase):
    phieudatchos: List["PhieuDatChoVeMayBayInDB"] = []

    @property
    def so_phieu_dat(self) -> int:
        return len(self.phieudatchos)

    @property
    def ngay_them_format(self) -> str:
        return self.ngaythem.strftime("%d/%m/%Y %H:%M")

    @property
    def trang_thai_hoat_dong(self) -> str:
        return "Đang hoạt động" if self.so_phieu_dat > 0 else "Chưa hoạt động"

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }
