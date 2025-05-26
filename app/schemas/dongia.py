from pydantic import BaseModel, Field
from typing import Optional
from .tuyenbay import TuyenBayInDB
from .hangve import HangVeInDB

class DonGiaBase(BaseModel):
    MADONGIA: str
    MATUYENBAY: str
    MAHANGVE: str
    GIATIEN: int = Field(..., gt=0)

    class Config:
        from_attributes = True

class DonGiaCreate(BaseModel):
    MATUYENBAY: str
    MAHANGVE: str
    GIATIEN: int = Field(..., gt=0)

    class Config:
        from_attributes = True

class DonGiaUpdate(BaseModel):
    MAHANGVE: str | None = None
    GIATIEN: int | None = Field(None, gt=0)

    class Config:
        from_attributes = True

class DonGiaInDB(DonGiaBase):
    tuyenbay: TuyenBayInDB
    hangve: HangVeInDB

    @property
    def gia_tien_format(self) -> str:
        return f"{self.GIATIEN:,} VNĐ"

    class Config:
        from_attributes = True 