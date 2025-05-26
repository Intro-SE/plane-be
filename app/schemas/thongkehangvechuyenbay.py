from pydantic import BaseModel, Field
from typing import Optional
from .chuyenbay import ChuyenBayInDB
from .hangve import HangVeInDB

class ThongKeHangVeChuyenBayBase(BaseModel):
    MATHONGKEHANGVECB: str
    MACHUYENBAY: str
    MAHANGVE: str
    SOLUONGGHE: int = Field(..., gt=0)
    SOGHETRONG: int = Field(..., ge=0)
    SOGHEDAT: int = Field(..., ge=0)

    class Config:
        from_attributes = True

class ThongKeHangVeChuyenBayCreate(BaseModel):
    MACHUYENBAY: str
    MAHANGVE: str
    SOLUONGGHE: int = Field(..., gt=0)
    SOGHETRONG: int = Field(..., ge=0)
    SOGHEDAT: int = Field(..., ge=0)

    class Config:
        from_attributes = True

class ThongKeHangVeChuyenBayUpdate(BaseModel):
    SOLUONGGHE: int | None = Field(None, gt=0)
    SOGHETRONG: int | None = Field(None, ge=0)
    SOGHEDAT: int | None = Field(None, ge=0)

    class Config:
        from_attributes = True

class ThongKeHangVeChuyenBayInDB(ThongKeHangVeChuyenBayBase):
    chuyenbay: ChuyenBayInDB
    hangve: HangVeInDB

    @property
    def ti_le_dat(self) -> float:
        if self.SOLUONGGHE == 0:
            return 0
        return (self.SOGHEDAT / self.SOLUONGGHE) * 100

    @property
    def ti_le_dat_format(self) -> str:
        return f"{self.ti_le_dat:.1f}%"

    class Config:
        from_attributes = True 