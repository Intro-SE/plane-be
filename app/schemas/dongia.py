from pydantic import BaseModel

class DonGiaBase(BaseModel):
    MADONGIA: str
    MATUYENBAY: str
    MAHANGVE: str
    GIATIEN: int

    class Config:
        from_attributes = True

class DonGiaCreate(DonGiaBase):
    pass

class DonGiaUpdate(DonGiaBase):
    pass

class DonGiaInDB(DonGiaBase):
    pass 