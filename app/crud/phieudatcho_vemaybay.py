from app.models.phieudatcho_vemaybay import PhieuDatChoVeMayBay
from app.models.chuyenbay import ChuyenBay
from app.models.tuyenbay import TuyenBay
from app.models.sanbay import SanBay
from app.models.hangve import HangVe
from app.models.taikhoannhanvien import TaiKhoanNhanVien
from app.schemas.phieudatcho_vemaybay import PhieuDatChoVeMayBayCreate, PhieuDatChoVeMayBayUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from typing import List
from datetime import datetime
from sqlalchemy import func
import re
from typing import Optional

async def get_all_tickets(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[PhieuDatChoVeMayBay]:
    result = await db.execute(
        select(PhieuDatChoVeMayBay)
        .options(
            joinedload(PhieuDatChoVeMayBay.hangve),
            joinedload(PhieuDatChoVeMayBay.nhanvien),
            joinedload(PhieuDatChoVeMayBay.chuyenbay)
                .joinedload(ChuyenBay.tuyenbay)
                .joinedload(TuyenBay.sanbay_di),
            joinedload(PhieuDatChoVeMayBay.chuyenbay)
                .joinedload(ChuyenBay.tuyenbay)
                .joinedload(TuyenBay.sanbay_den)
        )
        .offset(skip).limit(limit)
    )
    return result.unique().scalars().all()


async def get_id(db: AsyncSession, id_pdc: str) -> Optional[PhieuDatChoVeMayBay]:
    result = await db.execute(select(PhieuDatChoVeMayBay).where(PhieuDatChoVeMayBay.maphieudatcho == id_pdc))
    return result.unique().scalars().one_or_none()



async def generate_next_id(session):
    result = await session.execute(
        select(func.max(PhieuDatChoVeMayBay.maphieudatcho))
    )
    max_id = result.scalar()

    if not max_id:
        return "PDC01"
    
    match = re.search(r'PDC(\d+)', max_id)
    if match:
        next_num = int(match.group(1)) + 1
        return f"PDC{next_num:03d}" 

    
async def create_ticket(db: AsyncSession, ticket: PhieuDatChoVeMayBayCreate) -> PhieuDatChoVeMayBay:
    maphieudatcho = await generate_next_id(db)
    new_ticket = PhieuDatChoVeMayBay(
        maphieudatcho = maphieudatcho,
        machuyenbay=ticket.machuyenbay,
        tenhanhkhach=ticket.tenhanhkhach,
        cmnd_cccd=ticket.cmnd_cccd,
        gioitinh=ticket.gioitinh,
        sodienthoai=ticket.sodienthoai,
        mahangve=ticket.mahangve,
        giatien=ticket.giatien,
        trangthailayve=ticket.trangthailayve,
        idnhanvien=ticket.idnhanvien,
        ngaydat=datetime.now()
    )
    db.add(new_ticket)
    await db.commit()
    await db.refresh(new_ticket)
    return new_ticket


async def update_ticket(db: AsyncSession, db_ticket: PhieuDatChoVeMayBay, ticket: PhieuDatChoVeMayBayUpdate) -> PhieuDatChoVeMayBay:

    update_data = ticket.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ticket, key, value)

    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket

async def delete_ticket(db: AsyncSession,  obj_in: PhieuDatChoVeMayBay) -> Optional[PhieuDatChoVeMayBay]:
    if obj_in:
        await db.delete(obj_in)
        await db.commit()
    return obj_in