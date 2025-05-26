from sqlalchemy import Column, Integer, CheckConstraint
from app.models.base import Base

class Rules(Base):
    __tablename__ = "RULES"

    SOLUONGSANBAYTOIDA = Column(Integer, default=10)
    SOLUONGSANBAYTRUNGGIANTOIDA = Column(Integer, default=2)
    THOIGIANBAYTOITHIEU = Column(Integer, default=30)
    THOIGIANDUNGTOIDA = Column(Integer, default=20)
    THOIGIANDUNGTOITHIEU = Column(Integer, default=10)
    THOIGIANCHAMNHATDATVE = Column(Integer, default=1)
    THOIGIANCHAMNHATHUYDATVE = Column(Integer, default=1)

    __table_args__ = (
        CheckConstraint('SOLUONGSANBAYTOIDA >= 0'),
        CheckConstraint('SOLUONGSANBAYTRUNGGIANTOIDA >= 0'),
        CheckConstraint('THOIGIANBAYTOITHIEU > 0'),
        CheckConstraint('THOIGIANDUNGTOIDA >= THOIGIANDUNGTOITHIEU'),
        CheckConstraint('THOIGIANDUNGTOITHIEU > 0'),
        CheckConstraint('THOIGIANCHAMNHATDATVE > 0'),
        CheckConstraint('THOIGIANCHAMNHATHUYDATVE > 0'),
    ) 