from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from datetime import time

class ChuyenBayRef(BaseModel):
    machuyenbay: str
    matuyenbay: str
    ngaybay: date
    giobay: time
    thoigianbay: int
    soghechuyenbay: int

    class Config:
        from_attributes = True

class HangVeRef(BaseModel):
    mahangve: str
    tenhangve: str

    class Config:
        from_attributes = True

class NhanVienRef(BaseModel):
    idnhanvien: str
    tennhanvien: str
    sodienthoai: str

    class Config:
        from_attributes = True

class PhieuDatChoVeMayBayBase(BaseModel):
    maphieudatcho: str
    machuyenbay: str
    tenhanhkhach: str = Field(..., min_length=1, max_length=50)
    cmnd_cccd: str = Field(..., pattern=r'^\d{9}|\d{12}$')
    gioitinh: str = Field(..., pattern=r'^(Nam|Nữ)$')
    sodienthoai: str = Field(..., pattern=r'^\d{10}$')
    mahangve: str
    giatien: int = Field(..., gt=0)
    ngaydat: date
    trangthailayve: bool
    idnhanvien: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
            date: lambda v: v.strftime("%Y-%m-%d")
        }

class PhieuDatChoVeMayBayCreate(BaseModel):
    machuyenbay: str
    tenhanhkhach: str = Field(..., min_length=1, max_length=50)
    cmnd_cccd: str = Field(..., pattern=r'^\d{9}|\d{12}$')
    gioitinh: str = Field(..., pattern=r'^(Nam|Nữ)$')
    sodienthoai: str = Field(..., pattern=r'^\d{10}$')
    mahangve: str
    giatien: int = Field(..., gt=0)
    trangthailayve: bool = Field(default=False)
    idnhanvien: str

    class Config:
        from_attributes = True

class PhieuDatChoVeMayBayUpdate(BaseModel):
    tenhanhkhach: str | None = Field(None, min_length=1, max_length=50)
    cmnd_cccd: str | None = Field(None, pattern=r'^(\d{9}|\d{12})$')
    gioitinh: str | None = Field(None, pattern=r'^(Nam|Nữ)$')
    sodienthoai: str | None = Field(None, pattern=r'^\d{10}$')
    mahangve: str | None = None
    giatien: int | None = Field(None, gt=0)
    trangthailayve: bool | None = None

    class Config:
        from_attributes = True

class PhieuDatChoVeMayBayInDB(PhieuDatChoVeMayBayBase):
    chuyenbay: Optional[ChuyenBayRef] = None
    hangve: Optional[HangVeRef] = None
    nhanvien: Optional[NhanVienRef] = None

    @property
    def trang_thai_ve(self) -> str:
        return "Đã lấy vé" if self.trangthailayve else "Chưa lấy vé"

    @property
    def ngay_dat_format(self) -> str:
        return self.ngaydat.strftime("%d/%m/%Y")

    @property
    def gia_tien_format(self) -> str:
        return f"{self.giatien:,} VNĐ"

    class Config:
        from_attributes = True
        
        
class ThongTinHanhKhach(BaseModel):
    gioitinh: str
    cmnd_cccd: str
    tenhanhkhach: str
    sodienthoai: str
    
    
    
class VeChuyenBay(BaseModel):
    maphieudatcho: str
    machuyenbay: str
    tenhangve: str
    
    
    sanbay_di: str
    masanbay_di: str
    ngaybay: date
    giobay: time
    
    
    sanbay_den: str
    masanbay_den: str
    ngayden: str
    gioden:str
    
    thongtinhanhkhach: ThongTinHanhKhach
    giatien: int
    
    class Config:
        from_attributes = True
    
