from app.crud.flight import get_all_flight, create_flight, update_flight, delete_flight, get_id
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, status
from app.deps import get_db
from app.models.Flight import Flight
from app.schemas.Flight import FlightCreate, FlightInDB, FlightUpdate, FlightRouteRef, BookingTicketRef, TicketClassStatisticsRef

router = APIRouter()

@router.get("/", response_model=List[FlightInDB])
async def get_all_flights(skip:int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    try:
        flights = await get_all_flight(db, skip, limit)
        result = []
        for flight in flights:
            flight_route = FlightRouteRef(
                flight_route_id=flight.flight_route.flight_route_id,
                departure_airport=flight.flight_route.departure_airport.airport_name,
                departure_address=flight.flight_route.departure_airport.airport_address,
                arrival_airport=flight.flight_route.arrival_airport.airport_name,
                arrival_address=flight.flight_route.arrival_airport.airport_address
            )
            
            statics = []
            for static in flight.ticket_class_statistics:
                static_class_ticket = TicketClassStatisticsRef(
                    ticket_class_id=static.ticket_class.ticket_class_id,
                    ticket_class_name=static.ticket_class.ticket_class_name,
                    total_seats=static.total_seats,
                    available_seats = static.available_seats,
                    booked_seats = static.booked_seats
                )
                statics.append(static_class_ticket)
            
            flight_data = FlightInDB(
                flight_id=flight.flight_id,
                flight_route_id=flight.flight_route_id,
                departure_date=flight.flight_date,
                departure_time=flight.departure_time,
                duration=flight.flight_duration,
                total_seats=flight.flight_seat_count,
                flight_route=flight_route,
                ticket_class_statistics=statics
            )
            result.append(flight_data)
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    


@router.post("/", response_model=FlightInDB, status_code= status.HTTP_201_CREATED)
async def create_new_flight(flight: FlightCreate, db: AsyncSession = Depends(get_db)):
    try: 
        new_flight = await create_flight(db,flight)
        return new_flight
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))
    
    
@router.put("/", response_model=FlightInDB, status_code= status.HTTP_202_ACCEPTED)
async def update_info(flight_id: str, obj_in : FlightUpdate,db: AsyncSession = Depends(get_db)):
    db_obj = await get_id(db, flight_id)
    
    if not db_obj:
        raise HTTPException(status_code= 404, detail= "Flight not found")
    
    return await update_flight(db, db_obj, obj_in)

@router.delete("/", response_model=FlightInDB, status_code= status.HTTP_202_ACCEPTED)
async def delete_info(flight_id: str,db: AsyncSession = Depends(get_db)):
    db_obj = await get_id(db ,flight_id)
    
    if not db_obj:
        raise HTTPException(status_code= 404, detail= "Flight not found")
    
    return await delete_flight(db, db_obj)
