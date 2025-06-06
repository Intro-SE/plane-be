from sqlalchemy.ext.asyncio import AsyncSession
from app.models.TicketClass import TicketClass
from app.models.TicketClassStatistics import TicketClassStatistics
from app.models.TicketPrice import TicketPrice

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from typing import Optional, List



async def get_ticket_class(db: AsyncSession,flight_id: str, skip: int = 0, limit: int = 100) -> List[TicketClassStatistics]:
    result = await db.execute(select(TicketClassStatistics)
                            .options( selectinload(TicketClassStatistics.ticket_class),
                                     selectinload(TicketClassStatistics.ticket_class).selectinload(TicketClass.ticket_prices),)
                            .where(TicketClassStatistics.flight_id == flight_id).offset(skip).limit(limit))
    return result.unique().scalars().all()
