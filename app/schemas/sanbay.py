from pydantic import BaseModel, Field
from typing import List, Optional
from .tuyenbay import TuyenBayInDB
from .chitietchuyenbay import ChiTietChuyenBayInDB

class SanBayBase(BaseModel):
    MASANBAY: str
    TENSANBAY: str = Field(..., min_length=1, max_length=50)
    DIACHISANBAY: str = Field(..., min_length=1, max_length=50)

    class Config:
        from_attributes = True

class SanBayCreate(BaseModel):
    TENSANBAY: str = Field(..., min_length=1, max_length=50)
    DIACHISANBAY: str = Field(..., min_length=1, max_length=50)

    class Config:
        from_attributes = True

class SanBayUpdate(BaseModel):
    TENSANBAY: str | None = Field(None, min_length=1, max_length=50)
    DIACHISANBAY: str | None = Field(None, min_length=1, max_length=50)

    class Config:
        from_attributes = True

class SanBayInDB(SanBayBase):
    tuyenbay_di: List[TuyenBayInDB] = []
    tuyenbay_den: List[TuyenBayInDB] = []
    chitietchuyenbays: List[ChiTietChuyenBayInDB] = []

    @property
    def so_chuyen_bay_di(self) -> int:
        return len(self.tuyenbay_di)

    @property
    def so_chuyen_bay_den(self) -> int:
        return len(self.tuyenbay_den)

    @property
    def so_chuyen_bay_trung_gian(self) -> int:
        return len(self.chitietchuyenbays)

    class Config:
        from_attributes = True 