from fastapi import FastAPI, HTTPException, APIRouter, Depends, status
from app.crud.booking_ticket import get_all_tickets, create_ticket, get_id,update_ticket, delete_ticket
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.BookingTicket import PassengerInfo, FlightTicketInfo, BookingTicketInDB, BookingTicketCreate, BookingTicketUpdate
from typing import List
from datetime import date, datetime, timedelta
from app.deps import get_db


router = APIRouter()

@router.get("/", response_model=List[BookingTicketInDB])
async def read_all_tickets(skip: int = 0, limit: int = 1000, db: AsyncSession = Depends(get_db)):
    try:
        tickets = await get_all_tickets(db, skip, limit)
        return tickets
    except Exception as e:
        raise HTTPException(status_code= 500, detail=str(e))


@router.post("/", response_model=BookingTicketInDB, status_code= status.HTTP_201_CREATED)
async def create_new_ticket(ticket: BookingTicketCreate, db: AsyncSession = Depends(get_db)):
    try: 
        new_ticket = await create_ticket(db,ticket)
        return new_ticket
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))
    
    
@router.put("/", response_model=BookingTicketInDB, status_code= status.HTTP_202_ACCEPTED)
async def update_info(booking_ticket_id: str, obj_in : BookingTicketUpdate,db: AsyncSession = Depends(get_db)):
    db_obj = await get_id(db, booking_ticket_id)
    
    if not db_obj:
        raise HTTPException(status_code= 404, detail= "Ticket not found")
    
    return await update_ticket(db, db_obj, obj_in)

@router.delete("/", response_model=BookingTicketInDB, status_code= status.HTTP_202_ACCEPTED)
async def delete_info(booking_ticket_id: str,db: AsyncSession = Depends(get_db)):
    db_obj = await get_id(db ,booking_ticket_id)
    
    if not db_obj:
        raise HTTPException(status_code= 404, detail= "Ticket not found")
    
    return await delete_ticket(db, db_obj)
