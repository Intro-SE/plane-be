from pydantic import BaseModel, Field
from typing import List, Optional
from .sanbay import SanBayInDB
from .chuyenbay import ChuyenBayInDB
from .chitietchuyenbay import ChiTietChuyenBayInDB
from .dongia import DonGiaInDB

class TuyenBayBase(BaseModel):
    MATUYENBAY: str
    SANBAYDI: str
    SANBAYDEN: str

    class Config:
        from_attributes = True

class TuyenBayCreate(BaseModel):
    SANBAYDI: str
    SANBAYDEN: str

    class Config:
        from_attributes = True

class TuyenBayUpdate(BaseModel):
    SANBAYDI: str | None = None
    SANBAYDEN: str | None = None

    class Config:
        from_attributes = True

class TuyenBayInDB(TuyenBayBase):
    sanbay_di: SanBayInDB
    sanbay_den: SanBayInDB
    chuyenbays: List[ChuyenBayInDB] = []
    chitietchuyenbays: List[ChiTietChuyenBayInDB] = []
    dongias: List[DonGiaInDB] = []

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
        return min(dongia.GIATIEN for dongia in self.dongias)

    @property
    def gia_cao_nhat(self) -> int:
        if not self.dongias:
            return 0
        return max(dongia.GIATIEN for dongia in self.dongias)

    class Config:
        from_attributes = True 