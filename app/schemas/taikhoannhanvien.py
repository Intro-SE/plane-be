from pydantic import BaseModel
from datetime import datetime

class TaiKhoanNhanVienBase(BaseModel):
    IDNHANVIEN: str
    TENDANGNHAP: str
    MATKHAU: str
    TENNHANVIEN: str
    CMND_CCCD: str
    SODIENTHOAI: str
    GIOITINH: str | None = None
    NGAYTHEM: datetime

    class Config:
        from_attributes = True

class TaiKhoanNhanVienCreate(TaiKhoanNhanVienBase):
    pass

class TaiKhoanNhanVienUpdate(TaiKhoanNhanVienBase):
    pass

class TaiKhoanNhanVienInDB(TaiKhoanNhanVienBase):
    pass 