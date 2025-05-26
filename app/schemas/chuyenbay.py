from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from .tuyenbay import TuyenBayInDB
from .thongkehangvechuyenbay import ThongKeHangVeChuyenBayInDB
from .phieudatcho_vemaybay import PhieuDatChoVeMayBayInDB

class ChuyenBayBase(BaseModel):
    MACHUYENBAY: str
    MATUYENBAY: str
    NGAYBAY: datetime
    GIOBAY: datetime
    THOIGIANBAY: int = Field(..., gt=0)
    SOGHECHUYENBAY: int = Field(..., gt=0)

    class Config:
        from_attributes = True

class ChuyenBayCreate(BaseModel):
    MATUYENBAY: str
    NGAYBAY: datetime
    GIOBAY: datetime
    THOIGIANBAY: int = Field(..., gt=0)
    SOGHECHUYENBAY: int = Field(..., gt=0)

    class Config:
        from_attributes = True

class ChuyenBayUpdate(BaseModel):
    NGAYBAY: datetime | None = None
    GIOBAY: datetime | None = None
    THOIGIANBAY: int | None = Field(None, gt=0)
    SOGHECHUYENBAY: int | None = Field(None, gt=0)

    class Config:
        from_attributes = True

class ChuyenBayInDB(ChuyenBayBase):
    tuyenbay: TuyenBayInDB
    thongkehangves: List[ThongKeHangVeChuyenBayInDB] = []
    phieudatchos: List[PhieuDatChoVeMayBayInDB] = []

    @property
    def so_ve_da_dat(self) -> int:
        return len(self.phieudatchos)

    @property
    def so_ve_con_trong(self) -> int:
        return self.SOGHECHUYENBAY - self.so_ve_da_dat

    @property
    def ngay_gio_bay_format(self) -> str:
        return f"{self.NGAYBAY.strftime('%d/%m/%Y')} {self.GIOBAY.strftime('%H:%M')}"

    class Config:
        from_attributes = True 