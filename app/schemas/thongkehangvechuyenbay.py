from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING

class ThongKeHangVeChuyenBayBase(BaseModel):
    mathongkehangvecb: str
    machuyenbay: str
    mahangve: str
    soluongghe: int = Field(..., gt=0)
    soghetrong: int = Field(..., ge=0)
    soghedat: int = Field(..., ge=0)

    class Config:
        from_attributes = True

class ThongKeHangVeChuyenBayCreate(BaseModel):
    machuyenbay: str
    mahangve: str
    soluongghe: int = Field(..., gt=0)
    soghetrong: int = Field(..., ge=0)
    soghedat: int = Field(..., ge=0)

    class Config:
        from_attributes = True

class ThongKeHangVeChuyenBayUpdate(BaseModel):
    soluongghe: int | None = Field(None, gt=0)
    soghetrong: int | None = Field(None, ge=0)
    soghedat: int | None = Field(None, ge=0)

    class Config:
        from_attributes = True

class ThongKeHangVeChuyenBayInDB(ThongKeHangVeChuyenBayBase):
    chuyenbay: "ChuyenBayInDB"
    hangve: "HangVeInDB"

    @property
    def ti_le_dat(self) -> float:
        if self.soluongghe == 0:
            return 0
        return (self.soghedat / self.soluongghe) * 100

    @property
    def ti_le_dat_format(self) -> str:
        return f"{self.ti_le_dat:.1f}%"

    class Config:
        from_attributes = True

if TYPE_CHECKING:
    from .chuyenbay import ChuyenBayInDB
    from .hangve import HangVeInDB 