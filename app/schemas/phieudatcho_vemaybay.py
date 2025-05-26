from pydantic import BaseModel
from datetime import datetime

class PhieuDatChoVeMayBayBase(BaseModel):
    MAPHIEUDATCHO: str
    MACHUYENBAY: str
    TENHANHKHACH: str
    CMND_CCCD: str
    GIOITINH: str
    SODIENTHOAI: str
    MAHANGVE: str
    GIATIEN: int
    NGAYDAT: datetime
    TRANGTHAILAYVE: bool
    IDNHANVIEN: str

    class Config:
        from_attributes = True

class PhieuDatChoVeMayBayCreate(PhieuDatChoVeMayBayBase):
    pass

class PhieuDatChoVeMayBayUpdate(PhieuDatChoVeMayBayBase):
    pass

class PhieuDatChoVeMayBayInDB(PhieuDatChoVeMayBayBase):
    pass 