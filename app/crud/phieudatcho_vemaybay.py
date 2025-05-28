from app.models.phieudatcho_vemaybay import PhieuDatChoVeMayBay
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.phieudatcho_vemaybay import PhieuDatChoVeMayBayCreate, PhieuDatChoVeMayBayUpdate
from typing import Optional, List
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select, func
from sqlalchemy.future import select



