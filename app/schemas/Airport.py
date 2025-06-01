from pydantic import BaseModel, Field
from typing import List, Optional


class AirportInDB(BaseModel):
    airport_id: str
    airport_name: str = Field(..., min_length=1, max_length=50)
    airport_address: str = Field(..., min_length=1, max_length=50)

    class Config:
        from_attributes = True

class AirportCreate(BaseModel):
    airport_name: str = Field(..., min_length=1, max_length=50)
    airport_address: str = Field(..., min_length=1, max_length=50)

    class Config:
        from_attributes = True

class AirportUpdate(BaseModel):
    airport_name: Optional[str] = Field(None, min_length=1, max_length=50)
    airport_address: Optional[str] = Field(None, min_length=1, max_length=50)

    class Config:
        from_attributes = True
