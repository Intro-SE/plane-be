from pydantic import BaseModel, Field
from typing import List, Optional

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sanbay import SanBayInDB
    from .chuyenbay import ChuyenBayInDB
    from .chitietchuyenbay import ChiTietChuyenBayInDB
    from .dongia import DonGiaInDB
    
    
class TuyenBayBase(BaseModel):
    matuyenbay: str
    sanbaydi: str
    sanbayden: str

    class Config:
        from_attributes = True

class TuyenBayCreate(BaseModel):
    sanbaydi: str
    sanbayden: str

    class Config:
        from_attributes = True

class TuyenBayUpdate(BaseModel):
    sanbaydi: str | None = None
    sanbayden: str | None = None

    class Config:
        from_attributes = True

class TuyenBayInDB(TuyenBayBase):
    sanbay_di: "SanBayInDB"
    sanbay_den: "SanBayInDB"
    chuyenbays: List["ChuyenBayInDB"] = []
    chitietchuyenbays: List["ChiTietChuyenBayInDB"] = []
    dongias: List["DonGiaInDB"] = []

    @property
    def so_chuyen_bay(self) -> int:
        return len(self.chuyenbays)

    @property
    def so_san_bay_trung_gian(self) -> int:
        return len(self.chitietchuyenbays)

    @property
    def gia_thap_nhat(self) -> int:
        if not self.dongias:
            return 0
        return min(dongia.giatien for dongia in self.dongias)

    @property
    def gia_cao_nhat(self) -> int:
        if not self.dongias:
            return 0
        return max(dongia.giatien for dongia in self.dongias)

    class Config:
        from_attributes = True 
        
        
