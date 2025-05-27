from sqlalchemy.ext.asyncio import AsyncSession
from app.models.taikhoannhanvien import TaiKhoanNhanVien
from app.schemas.taikhoannhanvien import TaiKhoanNhanVienCreate, TaiKhoanNhanVienUpdate
from typing import Optional, List
from sqlalchemy.orm import selectinload,joinedload
from sqlalchemy import select, func
import re
from sqlalchemy.future import select


async def get_by_id(db: AsyncSession, id_nhanvien: str) -> Optional[TaiKhoanNhanVien]:
    result = await db.execute(
        select(TaiKhoanNhanVien)
        .options(joinedload(TaiKhoanNhanVien.phieudatchos))
        .where(TaiKhoanNhanVien.idnhanvien == id_nhanvien)
    )
    return result.unique().scalars().one_or_none()

async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100)-> List[TaiKhoanNhanVien]:
    result = await db.execute(select(TaiKhoanNhanVien)
                            .options(selectinload(TaiKhoanNhanVien.phieudatchos))
                            .offset(skip).limit(limit))
    return result.scalars().all()



async def generate_next_id(session):
    result = await session.execute(
        select(func.max(TaiKhoanNhanVien.idnhanvien))
    )
    max_id = result.scalar()

    if not max_id:
        return "NV001"
    
    match = re.search(r'NV(\d+)', max_id)
    if match:
        next_num = int(match.group(1)) + 1
        return f"NV{next_num:03d}" 
    else:
        raise ValueError("Mã nhân viên hiện tại không đúng định dạng 'NVxxx'")
    
async def create(db: AsyncSession, obj_in: TaiKhoanNhanVienCreate) -> TaiKhoanNhanVien:
    new_id = await generate_next_id(db)  
    
    db_obj = TaiKhoanNhanVien(
        idnhanvien=new_id,            
        **obj_in.dict()
    )
    
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update(db: AsyncSession, db_obj: TaiKhoanNhanVien, obj_in: TaiKhoanNhanVienUpdate) -> TaiKhoanNhanVien:
    update_data = obj_in.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def remove(db: AsyncSession, id_nhanvien: str) -> Optional[TaiKhoanNhanVien]:
    obj = await get_by_id(db, id_nhanvien)
    
    if obj:
        await db.delete(obj)
        await db.commit()
    return obj