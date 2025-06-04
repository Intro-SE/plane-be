    
    
from sqlalchemy.ext.asyncio import AsyncSession
from app.functions.flight_management import find_flights_by_filter, FlightCreate, create_new_flight, update_flight, delete_flight
from typing import Optional, List
from fastapi import APIRouter, HTTPException, status, Depends
from app.deps import get_db
from app.schemas.Flight import FlightOut,IntermediateStop, SeatInformation
from datetime import datetime, timedelta
from app.functions.flight_lookup import FlightSearch

router = APIRouter()
    
@router.post("/search", response_model=List[FlightOut])
async def search_flights(filters: FlightSearch, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
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
    
    
@router.post("/create", response_model=FlightOut)
async def create_flight(flight: FlightCreate, db: AsyncSession = Depends(get_db)):
    try:
        flight = await create_new_flight(db, flight)
        
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
        
            
        return flight_data
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))
    
    
    
@router.put("/update",response_model= FlightOut)
async def update(flight: FlightCreate, db: AsyncSession = Depends(get_db)):
    try:
        flight = await update_flight(db, flight)
        
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
        
            
        return flight_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.delete("/delete")
async def delete_flights(flight_ids: List[str], db: AsyncSession = Depends(get_db)):
    message = await delete_flight(flight_ids, db)
    return {"log": message}