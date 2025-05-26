from pydantic import BaseModel

class ThongKeHangVeChuyenBayBase(BaseModel):
    MATHONGKEHANGVECB: str
    MACHUYENBAY: str
    MAHANGVE: str
    SOLUONGGHE: int
    SOGHETRONG: int
    SOGHEDAT: int

    class Config:
        from_attributes = True

class ThongKeHangVeChuyenBayCreate(ThongKeHangVeChuyenBayBase):
    pass

class ThongKeHangVeChuyenBayUpdate(ThongKeHangVeChuyenBayBase):
    pass

class ThongKeHangVeChuyenBayInDB(ThongKeHangVeChuyenBayBase):
    pass 