from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING

class ChiTietChuyenBayBase(BaseModel):
    machitietchuyenbay: str
    matuyenbay: str
    masanbaytrunggian: str
    thoigiandung: int = Field(..., gt=0)
    ghichu: str | None = None

    class Config:
        from_attributes = True

class ChiTietChuyenBayCreate(BaseModel):
    matuyenbay: str
    masanbaytrunggian: str
    thoigiandung: int = Field(..., gt=0)
    ghichu: str | None = None

    class Config:
        from_attributes = True

class ChiTietChuyenBayUpdate(BaseModel):
    thoigiandung: int | None = Field(None, gt=0)
    ghichu: str | None = None

    class Config:
        from_attributes = True

class ChiTietChuyenBayInDB(ChiTietChuyenBayBase):
    tuyenbay: "TuyenBayInDB"
    sanbaytrunggian: "SanBayInDB"

    @property
    def thoi_gian_dung_format(self) -> str:
        return f"{self.thoigiandung} phút"

    class Config:
        from_attributes = True

if TYPE_CHECKING:
    from .tuyenbay import TuyenBayInDB
    from .sanbay import SanBayInDB 