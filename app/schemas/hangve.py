from pydantic import BaseModel, Field
from typing import List, Optional, TYPE_CHECKING


class HangVeBase(BaseModel):
    mahangve: str
    tenhangve: str = Field(..., min_length=1, max_length=50)

    class Config:
        from_attributes = True

class HangVeCreate(BaseModel):
    tenhangve: str = Field(..., min_length=1, max_length=50)

    class Config:
        from_attributes = True

class HangVeUpdate(BaseModel):
    tenhangve: str | None = Field(None, min_length=1, max_length=50)

    class Config:
        from_attributes = True

class HangVeInDB(HangVeBase):
    thongkehangves: List["ThongKeHangVeChuyenBayInDB"] = []
    dongias: List["DonGiaInDB"] = []
    phieudatchos: List["PhieuDatChoVeMayBayInDB"] = []

    @property
    def so_ve_da_dat(self) -> int:
        return len(self.phieudatchos)

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

if TYPE_CHECKING:
    from .thongkehangvechuyenbay import ThongKeHangVeChuyenBayInDB
    from .dongia import DonGiaInDB
    from .phieudatcho_vemaybay import PhieuDatChoVeMayBayInDB