from sqlalchemy import Column, Integer, CheckConstraint
from app.models.base import Base

class Rules(Base):
    __tablename__ = "rules"

    soluongsanbaytoida = Column(Integer, default=10)
    soluongsanbaytrunggiantoida = Column(Integer, default=2)
    thoigianbaytoithieu = Column(Integer, default=30)
    thoigiandungtoida = Column(Integer, default=20)
    thoigiandungtoithieu = Column(Integer, default=10)
    thoigianchamnhatdatve = Column(Integer, default=1)
    thoigianchamnhathuydatve = Column(Integer, default=1)

    __table_args__ = (
        CheckConstraint('soluongsanbaytoida >= 0'),
        CheckConstraint('soluongsanbaytrunggiantoida >= 0'),
        CheckConstraint('thoigianbaytoithieu > 0'),
        CheckConstraint('thoigiandungtoida >= thoigiandungtoithieu'),
        CheckConstraint('thoigiandungtoithieu > 0'),
        CheckConstraint('thoigianchamnhatdatve > 0'),
        CheckConstraint('thoigianchamnhathuydatve > 0'),
    ) 