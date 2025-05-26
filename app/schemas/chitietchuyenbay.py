from pydantic import BaseModel, Field
from typing import Optional
from .tuyenbay import TuyenBayInDB
from .sanbay import SanBayInDB

class ChiTietChuyenBayBase(BaseModel):
    MACHITIETCHUYENBAY: str
    MATUYENBAY: str
    MASANBAYTRUNGGIAN: str
    THOIGIANDUNG: int = Field(..., gt=0)
    GHICHU: str | None = None

    class Config:
        from_attributes = True

class ChiTietChuyenBayCreate(BaseModel):
    MATUYENBAY: str
    MASANBAYTRUNGGIAN: str
    THOIGIANDUNG: int = Field(..., gt=0)
    GHICHU: str | None = None

    class Config:
        from_attributes = True

class ChiTietChuyenBayUpdate(BaseModel):
    MASANBAYTRUNGGIAN: str | None = None
    THOIGIANDUNG: int | None = Field(None, gt=0)
    GHICHU: str | None = None

    class Config:
        from_attributes = True

class ChiTietChuyenBayInDB(ChiTietChuyenBayBase):
    tuyenbay: TuyenBayInDB
    sanbaytrunggian: SanBayInDB

    @property
    def thoi_gian_dung_format(self) -> str:
        return f"{self.THOIGIANDUNG} phút"

    class Config:
        from_attributes = True 