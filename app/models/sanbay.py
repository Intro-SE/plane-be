from sqlalchemy import Column, String
from app.models.base import Base

class SanBay(Base):
    __tablename__ = "SANBAY"

    MASANBAY = Column(String(50), primary_key=True)
    TENSANBAY = Column(String(50), nullable=False)
    DIACHISANBAY = Column(String(50), nullable=False) 