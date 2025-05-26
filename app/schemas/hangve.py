from pydantic import BaseModel

class HangVeBase(BaseModel):
    MAHANGVE: str
    TENHANGVE: str

    class Config:
        from_attributes = True

class HangVeCreate(HangVeBase):
    pass

class HangVeUpdate(HangVeBase):
    pass

class HangVeInDB(HangVeBase):
    pass 