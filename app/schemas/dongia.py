from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING

class DonGiaBase(BaseModel):
    madongia: str
    matuyenbay: str
    mahangve: str
    giatien: int = Field(..., gt=0)

    class Config:
        from_attributes = True

class DonGiaCreate(BaseModel):
    matuyenbay: str
    mahangve: str
    giatien: int = Field(..., gt=0)

    class Config:
        from_attributes = True

class DonGiaUpdate(BaseModel):
    giatien: int | None = Field(None, gt=0)

    class Config:
        from_attributes = True

class DonGiaInDB(DonGiaBase):
    tuyenbay: "TuyenBayInDB"
    hangve: "HangVeInDB"

    @property
    def gia_tien_format(self) -> str:
        return f"{self.giatien:,} VNĐ"

    class Config:
        from_attributes = True

if TYPE_CHECKING:
    from .tuyenbay import TuyenBayInDB
    from .hangve import HangVeInDB 