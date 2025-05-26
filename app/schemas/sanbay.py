from pydantic import BaseModel

class SanBayBase(BaseModel):
    MASANBAY: str
    TENSANBAY: str
    DIACHISANBAY: str

    class Config:
        from_attributes = True

class SanBayCreate(SanBayBase):
    pass

class SanBayUpdate(SanBayBase):
    pass

class SanBayInDB(SanBayBase):
    pass 