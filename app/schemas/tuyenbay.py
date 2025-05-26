from pydantic import BaseModel

class TuyenBayBase(BaseModel):
    MATUYENBAY: str
    SANBAYDI: str
    SANBAYDEN: str

    class Config:
        from_attributes = True

class TuyenBayCreate(TuyenBayBase):
    pass

class TuyenBayUpdate(TuyenBayBase):
    pass

class TuyenBayInDB(TuyenBayBase):
    pass 