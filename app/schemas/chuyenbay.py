from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class ChuyenBayBase(BaseModel):
    machuyenbay: str
    matuyenbay: str
    ngaybay: datetime
    giobay: datetime
    thoigianbay: int = Field(..., gt=0)
    soghechuyenbay: int = Field(..., gt=0)

    class Config:
        from_attributes = True

class ChuyenBayCreate(BaseModel):
    matuyenbay: str
    ngaybay: datetime
    giobay: datetime
    thoigianbay: int = Field(..., gt=0)
    soghechuyenbay: int = Field(..., gt=0)

    class Config:
        from_attributes = True

class ChuyenBayUpdate(BaseModel):
    ngaybay: datetime | None = None
    giobay: datetime | None = None
    thoigianbay: int | None = Field(None, gt=0)
    soghechuyenbay: int | None = Field(None, gt=0)

    class Config:
        from_attributes = True

class ChuyenBayInDB(ChuyenBayBase):
    tuyenbay: "TuyenBayInDB"
    thongkehangves: List["ThongKeHangVeChuyenBayInDB"] = []
    phieudatchos: List["PhieuDatChoVeMayBayInDB"] = []

    @property
    def so_ve_da_dat(self) -> int:
        return len(self.phieudatchos)

    @property
    def so_ve_con_trong(self) -> int:
        return self.soghechuyenbay - self.so_ve_da_dat

    @property
    def ngay_gio_bay_format(self) -> str:
        return f"{self.ngaybay.strftime('%d/%m/%Y')} {self.giobay.strftime('%H:%M')}"

    class Config:
        from_attributes = True 
        
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .tuyenbay import TuyenBayInDB
    from .thongkehangvechuyenbay import ThongKeHangVeChuyenBayInDB
    from .phieudatcho_vemaybay import PhieuDatChoVeMayBayInDB