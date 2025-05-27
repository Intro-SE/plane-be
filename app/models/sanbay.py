from sqlalchemy import Column, String
from app.models.base import Base

class SanBay(Base):
    __tablename__ = "sanbay"

    masanbay = Column(String(50), primary_key=True)
    tensanbay = Column(String(50), nullable=False)
    diachisanbay = Column(String(50), nullable=False) 