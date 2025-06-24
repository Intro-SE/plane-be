from sqlalchemy.ext.asyncio import AsyncSession
from app.functions.flight_lookup import get_all_flights, find_flights_by_filter
from typing import Optional, List
from fastapi import APIRouter, HTTPException, status, Depends
from app.deps import get_db
from app.schemas.Flight import FlightOut,IntermediateStop, SeatInformation,TicketClassStatisticsRef
from datetime import datetime, timedelta
from pydantic import BaseModel
from app.functions.flight_lookup import FlightSearch

router = APIRouter()





@router.get("/", response_model=List[FlightOut])
async def get_all(skip: int = 0, limit: int = 1000, db : AsyncSession = Depends(get_db)):
    try:
        flights = await get_all_flights(db, skip, limit)
        result = []      
        for flight in flights:

            intermediate_stops = [
                IntermediateStop(
                    stop_number=idx + 1,
                    stop_name=detail.transit_airport.airport_name,
                    stop_time=detail.stop_time,
                    note = detail.note
                )
                for idx, detail in enumerate(flight.flight_route.flight_details)
            ]

            seat_info = SeatInformation(
                seat_type=[stat.ticket_class.ticket_class_name for stat in flight.ticket_class_statistics],
                seat_price=[
                    stat.ticket_class.ticket_prices[0].price if stat.ticket_class.ticket_prices else 0
                    for stat in flight.ticket_class_statistics
                ],
                total_type_seats=[stat.total_seats for stat in flight.ticket_class_statistics],
                empty_type_seats=[stat.available_seats for stat in flight.ticket_class_statistics],
                occupied_type_seats =[stat.booked_seats for stat in flight.ticket_class_statistics] ,
                empty_seats=sum(stat.available_seats for stat in flight.ticket_class_statistics),
                occupied_seats=sum(stat.booked_seats for stat in flight.ticket_class_statistics),
            )
            
            flight_data = FlightOut(
                flight_id=flight.flight_id,
                flight_route_id= flight.flight_route_id,
                departure_date=flight.flight_date,
                total_seats=flight.flight_seat_count,

                departure_address=flight.flight_route.departure_airport.airport_address,
                departure_time=flight.departure_time,
                departure_airport=flight.flight_route.departure_airport.airport_name,

                arrival_time = (datetime.combine(flight.flight_date, flight.departure_time)+ timedelta(minutes=flight.flight_duration)).time(),
                arrival_airport=flight.flight_route.arrival_airport.airport_name,
                arrival_address=flight.flight_route.arrival_airport.airport_address,
                
                intermediate_stops=intermediate_stops,
                seat_information=seat_info
            )
            result.append(flight_data)
            
        return result
        
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.post("/search", response_model=List[FlightOut])
async def search_flights(filters: FlightSearch, skip: int = 0, limit: int = 1000, db: AsyncSession = Depends(get_db)):
    try:
        flights = await find_flights_by_filter(db, filters, skip, limit)
        result = []      
        for flight in flights:

            intermediate_stops = [
                IntermediateStop(
                    stop_number=idx + 1,
                    stop_name=detail.transit_airport.airport_name,
                    stop_time=detail.stop_time,
                    note = detail.note
                )
                for idx, detail in enumerate(flight.flight_route.flight_details)
            ]

            seat_info = SeatInformation(
                seat_type=[stat.ticket_class.ticket_class_name for stat in flight.ticket_class_statistics],
                seat_price=[
                    stat.ticket_class.ticket_prices[0].price if stat.ticket_class.ticket_prices else 0
                    for stat in flight.ticket_class_statistics
                ],
                empty_type_seats=[stat.available_seats for stat in flight.ticket_class_statistics],
                empty_seats=sum(stat.available_seats for stat in flight.ticket_class_statistics),
                occupied_seats=sum(stat.booked_seats for stat in flight.ticket_class_statistics),
            )
            
            flight_data = FlightOut(
                flight_id=flight.flight_id,
                departure_date=flight.flight_date,
                total_seats=flight.flight_seat_count,

                departure_address=flight.flight_route.departure_airport.airport_address,
                departure_time=flight.departure_time,
                departure_airport=flight.flight_route.departure_airport.airport_name,

                arrival_time = (datetime.combine(flight.flight_date, flight.departure_time)+ timedelta(minutes=flight.flight_duration)).time(),
                arrival_airport=flight.flight_route.arrival_airport.airport_name,
                arrival_address=flight.flight_route.arrival_airport.airport_address,
                
                intermediate_stops=intermediate_stops,
                seat_information=seat_info
            )
            result.append(flight_data)
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))