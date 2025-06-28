from app.models.Flight import Flight
from app.models.FlightRoute import FlightRoute
from app.models.FlightDetail import FlightDetail
from typing import Optional, List, Dict, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy.orm import selectinload
from app.models.TicketClassStatistics import TicketClassStatistics
from app.models.FlightRoute import FlightRoute
from app.models.TicketClass import TicketClass
from pydantic import BaseModel, validator,model_validator
from datetime import datetime, time, date
from sqlalchemy import select, and_, or_, func
from app.functions.flight_lookup import FlightSearch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import re
from app.models.Rules import Rules
from app.models.TicketPrice import TicketPrice

    
async def generate_next_id(session):
    result = await session.execute(select(TicketClassStatistics.ticket_class_statistics_id))
    ids = [row[0] for row in result.all()]

    max_num = 0
    for bid in ids:
        match = re.search(r'TK(\d+)', bid)
        if match:
            num = int(match.group(1))
            max_num = max(max_num, num)

    next_num = max_num + 1
    return f"TK{next_num:03d}" 

class FlightCreate(BaseModel):
    flight_id : Optional[str] = None
    flight_route: Optional[str] = None
    departure_airport: Optional[str] = None
    arrival_airport: Optional[str] = None
    departure_date: Optional[date] = None
    departure_time : Optional[time] = None
    flight_duration: Optional[int] = None
    total_seats: Optional[int] = None
    
    seat_type : Optional[List[str]] = None
    total_type_seats: Optional[List[int]] = None
    
    
    class Config:
        from_attributes = True
    
    @model_validator(mode="after")
    def check_logic_seats(cls, values):
        if values.total_seats and values.total_type_seats:
            if sum(values.total_type_seats) != values.total_seats:
                raise ValueError("Sum of total_type_seats must equal total_seats")
        return values

# Lấy tất cả các chuyến bay
async def get_all_flights(db: AsyncSession, skip: int = 0, limit: int = 1000) -> Tuple[List[Flight], Dict[Tuple[str, str], int]]:
    # Preload toàn bộ TicketPrice một lần duy nhất
    price_result = await db.execute(select(TicketPrice))
    all_prices = price_result.scalars().all()
    price_map = {
        (tp.flight_route_id, tp.ticket_class_id): tp.price
        for tp in all_prices
    }

    # Load Flight + các quan hệ cần thiết
    result = await db.execute(
        select(Flight)
        .options(
            selectinload(Flight.flight_route).selectinload(FlightRoute.departure_airport),
            selectinload(Flight.flight_route).selectinload(FlightRoute.arrival_airport),
            selectinload(Flight.flight_route).selectinload(FlightRoute.flight_details).selectinload(FlightDetail.transit_airport),
            selectinload(Flight.ticket_class_statistics).selectinload(TicketClassStatistics.ticket_class)
        )
        .offset(skip).limit(limit)
    )

    flights = result.scalars().all()
    return flights, price_map

# Tìm kiếm các chuyến bay theo bộ lọc
async def find_flights_by_filter(db: AsyncSession, filters: FlightSearch, skip: int = 0, limit: int = 1000) -> Tuple[List[Flight], Dict[Tuple[str, str], int]]:
    conditions = []

    if filters.flight_id:
        conditions.append(Flight.flight_id == filters.flight_id)

    if filters.departure_address:
        conditions.append(
            Flight.flight_route.has(
                FlightRoute.departure_airport.has(airport_address=filters.departure_address)
            )
        )

    if filters.arrival_address:
        conditions.append(
            Flight.flight_route.has(
                FlightRoute.arrival_airport.has(airport_address=filters.arrival_address)
            )
        )

    if filters.departure_date:
        conditions.append(Flight.flight_date == filters.departure_date)

    if filters.min_time:
        conditions.append(Flight.departure_time >= filters.min_time)

    if filters.max_time:
        conditions.append(Flight.departure_time <= filters.max_time)

    if filters.least_empty_seats:
        conditions.append(
            Flight.ticket_class_statistics.any(
                TicketClassStatistics.available_seats >= filters.least_empty_seats
            )
        )

    if filters.total_seats:
        conditions.append(Flight.flight_seat_count >= filters.total_seats)

    if filters.is_empty:
        conditions.append(Flight.ticket_class_statistics.any(TicketClassStatistics.available_seats > 0))

    query = (
        select(Flight)
        .options(
            selectinload(Flight.flight_route).selectinload(FlightRoute.departure_airport),
            selectinload(Flight.flight_route).selectinload(FlightRoute.arrival_airport),
            selectinload(Flight.flight_route).selectinload(FlightRoute.flight_details).selectinload(FlightDetail.transit_airport),
            selectinload(Flight.ticket_class_statistics).selectinload(TicketClassStatistics.ticket_class)
        )
    )

    if conditions:
        query = query.where(and_(*conditions))

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    flights = result.scalars().all()

    # Truy vấn ticket prices cho dict
    price_result = await db.execute(select(TicketPrice))
    all_prices = price_result.scalars().all()
    price_map = {
        (tp.flight_route_id, tp.ticket_class_id): tp.price
        for tp in all_prices
    }

    return flights, price_map





async def create_new_flight(db: AsyncSession, flight: FlightCreate) -> Flight:
    # 1. Truy vấn tuyến bay
    result = await db.execute(
        select(FlightRoute)
        .where(FlightRoute.flight_route_id == flight.flight_route)
        .options(
            selectinload(FlightRoute.departure_airport),
            selectinload(FlightRoute.arrival_airport),
            selectinload(FlightRoute.flight_details),
        )
    )
    route = result.unique().scalar_one_or_none()
    if not route:
        raise HTTPException(status_code=404, detail="Flight route not found")

    # 2. Lấy quy định hệ thống
    rules_result = await db.execute(select(Rules))
    rules = rules_result.scalar_one_or_none()
    if not rules:
        raise HTTPException(status_code=500, detail="Rules not found")

    # 3. Check thời gian bay tối thiểu
    if flight.flight_duration < rules.min_flight_time:
        raise HTTPException(status_code=400, detail=f"Flight duration must be at least {rules.min_flight_time} minutes")

    # 4. Check số lượng sân bay trung gian
    num_stops = len(route.flight_details)
    if num_stops > rules.max_transit_airports:
        raise HTTPException(status_code=400, detail=f"Too many transit airports: max is {rules.max_transit_airports}")

    # 5. Check thời gian dừng tại sân bay trung gian
    for detail in route.flight_details:
        if detail.stop_time < rules.min_stop_time or detail.stop_time > rules.max_stop_time:
            raise HTTPException(
                status_code=400,
                detail=f"Stop duration at airport '{detail.transit_airport_id}' must be between {rules.min_stop_time} and {rules.max_stop_time} minutes"
            )

    # 6. Check danh sách các hạng vé của tuyến bay
    ticket_prices_result = await db.execute(
        select(TicketPrice)
        .where(TicketPrice.flight_route_id == route.flight_route_id)
        .options(selectinload(TicketPrice.ticket_class))
    )
    ticket_prices = ticket_prices_result.scalars().all()
    route_ticket_classes = {tp.ticket_class.ticket_class_name for tp in ticket_prices}

    # 7. Kiểm tra số lượng hạng vé nhập có vượt quá số lượng hạng vé của tuyến bay được nhập không
    if len(flight.seat_type) > len(route_ticket_classes):
        raise HTTPException(
            status_code=400,
            detail=f"Too many ticket classes in flight. Max allowed for this route: {len(route_ticket_classes)}"
        )

    # 8. Kiểm tra các hạng vé có thuộc danh sách hạng vé của tuyến bay hay không
    for seat_class in flight.seat_type:
        if seat_class not in route_ticket_classes:
            raise HTTPException(
                status_code=400,
                detail=f"Ticket class '{seat_class}' is not available for the route"
            )

    # 8.5. Phải có ít nhất một hạng vé và độ dài danh sách khớp nhau
    if not flight.seat_type or not flight.total_type_seats:
        raise HTTPException(
            status_code=400,
            detail="At least one ticket class must be specified for the flight"
        )
    if len(flight.seat_type) != len(flight.total_type_seats):
        raise HTTPException(
            status_code=400,
            detail="Mismatch between number of ticket classes and seat counts"
        )


    # 9. Lấy tên sân bay đi và đến để hiển thị (không lưu)
    flight.departure_airport = route.departure_airport.airport_name
    flight.arrival_airport = route.arrival_airport.airport_name

    # 10. Check mã chuyến bay đã tồn tại chưa
    check = await db.execute(select(Flight).where(Flight.flight_id == flight.flight_id))
    if check.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Flight already exists")
    
    # 10.5 Check total_seats phải lớn hơn 0
    if flight.total_seats is None or flight.total_seats <= 0:
        raise HTTPException(
            status_code=400,
            detail="Flight must have at least 1 seat"
        )

    # 11. Tạo chuyến bay mới
    new_flight = Flight(
        flight_id=flight.flight_id,
        flight_route_id=flight.flight_route,
        flight_date=flight.departure_date,
        departure_time=flight.departure_time,
        flight_duration=flight.flight_duration,
        flight_seat_count=flight.total_seats
    )
    db.add(new_flight)

    # 12. Tạo thống kê cho từng hạng vé
    for type_name, total_seat in zip(flight.seat_type, flight.total_type_seats):
        result = await db.execute(select(TicketClass).where(TicketClass.ticket_class_name == type_name))
        ticket_class = result.unique().scalar_one_or_none()
        if not ticket_class:
            raise HTTPException(status_code=404, detail=f"Ticket class '{type_name}' does not exist")

        ticket_class_statistics_id = await generate_next_id(db)
        stats = TicketClassStatistics(
            ticket_class_statistics_id=ticket_class_statistics_id,
            flight_id=flight.flight_id,
            ticket_class_id=ticket_class.ticket_class_id,
            total_seats=total_seat,
            available_seats=total_seat,
            booked_seats=0
        )
        db.add(stats)

    # 13. Tạo dict ánh xạ (ticket_class_name, flight_route_id) → price
    price_map = {
        (tp.flight_route_id, tp.ticket_class_id): tp.price
        for tp in ticket_prices
    }

    # 14. Commit
    await db.commit()

    # 15. Load lại flight đã tạo
    result = await db.execute(
        select(Flight)
        .where(Flight.flight_id == flight.flight_id)
        .options(
            selectinload(Flight.flight_route).selectinload(FlightRoute.departure_airport),
            selectinload(Flight.flight_route).selectinload(FlightRoute.arrival_airport),
            selectinload(Flight.flight_route).selectinload(FlightRoute.flight_details).selectinload(FlightDetail.transit_airport),
            selectinload(Flight.ticket_class_statistics).selectinload(TicketClassStatistics.ticket_class).selectinload(TicketClass.ticket_prices)
        )
    )
    refreshed_flight = result.unique().scalar_one()
    return refreshed_flight, price_map





async def update_flight(db: AsyncSession, flight: FlightCreate) -> Flight:
    # Truy xuất chuyến bay cần cập nhật
    result = await db.execute(
        select(Flight)
        .where(Flight.flight_id == flight.flight_id)
        .options(
            selectinload(Flight.flight_route).selectinload(FlightRoute.departure_airport),
            selectinload(Flight.flight_route).selectinload(FlightRoute.arrival_airport),
            selectinload(Flight.ticket_class_statistics).selectinload(TicketClassStatistics.ticket_class)
        )
    )
    exist_flight = result.unique().scalar_one_or_none()
    if not exist_flight:
        raise HTTPException(status_code=404, detail="Flight not exists")

    route = exist_flight.flight_route

    # Lấy quy định hệ thống
    rules_result = await db.execute(select(Rules))
    rules = rules_result.unique().scalars().first()
    if not rules:
        raise HTTPException(status_code=500, detail="Rules not found")

    if flight.flight_duration < rules.min_flight_time:
        raise HTTPException(status_code=400, detail=f"Flight duration must be at least {rules.min_flight_time} minutes")

    num_stops = len(route.flight_details)
    if num_stops > rules.max_transit_airports:
        raise HTTPException(status_code=400, detail=f"Too many transit airports: max is {rules.max_transit_airports}")

    for detail in route.flight_details:
        if detail.stop_time < rules.min_stop_time or detail.stop_time > rules.max_stop_time:
            raise HTTPException(
                status_code=400,
                detail=f"Stop duration at airport '{detail.transit_airport_id}' must be between {rules.min_stop_time} and {rules.max_stop_time} minutes"
            )

    # Kiểm tra hạng vé tuyến bay và chuyến bay
    ticket_prices_result = await db.execute(
        select(TicketPrice)
        .where(TicketPrice.flight_route_id == route.flight_route_id)
        .options(selectinload(TicketPrice.ticket_class))
    )
    ticket_prices = ticket_prices_result.scalars().all()
    route_ticket_classes = {tp.ticket_class.ticket_class_name for tp in ticket_prices}

    if len(flight.seat_type) > len(route_ticket_classes):
        raise HTTPException(
            status_code=400,
            detail=f"Too many ticket classes in flight. Max allowed for this route: {len(route_ticket_classes)}"
        )

    for seat_class in flight.seat_type:
        if seat_class not in route_ticket_classes:
            raise HTTPException(
                status_code=400,
                detail=f"Ticket class '{seat_class}' is not assigned to this route"
            )
        
    # Kiểm tra phải có ít nhất một hạng vé
    if not flight.seat_type or not flight.total_type_seats:
        raise HTTPException(status_code=400, detail="Flight must have at least one ticket class")
    if len(flight.seat_type) != len(flight.total_type_seats):
        raise HTTPException(status_code=400, detail="Mismatch between ticket classes and seat counts")

    # Tính tổng số ghế đã đặt (booked_seats) hiện tại
    total_booked = sum(stat.booked_seats for stat in exist_flight.ticket_class_statistics)

    # Kiểm tra tổng ghế sau khi cập nhật không được < số ghế đã đặt
    if flight.total_seats is None or flight.total_seats < total_booked:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot set total seats to {flight.total_seats} (already booked: {total_booked})"
        )

    # Cập nhật thông tin chuyến bay
    exist_flight.flight_route_id = flight.flight_route
    exist_flight.flight_date = flight.departure_date
    exist_flight.departure_time = flight.departure_time
    exist_flight.flight_duration = flight.flight_duration
    exist_flight.flight_seat_count = flight.total_seats

    # Gán lại tên sân bay cho FE
    flight.departure_airport = exist_flight.flight_route.departure_airport.airport_name
    flight.arrival_airport = exist_flight.flight_route.arrival_airport.airport_name

    # Lấy thông tin thống kê ghế hiện có
    result = await db.execute(
        select(TicketClassStatistics)
        .options(selectinload(TicketClassStatistics.ticket_class))
        .where(TicketClassStatistics.flight_id == flight.flight_id)
    )
    existing_stats = {stat.ticket_class.ticket_class_name: stat for stat in result.scalars().all()}

    # Xóa các thống kê hạng vé không còn tồn tại trong seat_type mới
    for class_name in list(existing_stats.keys()):
        if class_name not in flight.seat_type:
            stat_to_delete = existing_stats[class_name]
            await db.delete(stat_to_delete)
            del existing_stats[class_name]


    # Cập nhật hoặc thêm thống kê hạng vé
    for type_name, new_total_seats in zip(flight.seat_type, flight.total_type_seats):
        result = await db.execute(select(TicketClass).where(TicketClass.ticket_class_name == type_name))
        ticket_class = result.unique().scalars().first()
        if not ticket_class:
            raise HTTPException(status_code=404, detail=f"Ticket class {type_name} not exists")

        if type_name in existing_stats:
            stat = existing_stats[type_name]
            if new_total_seats < stat.booked_seats:
                raise HTTPException(
                    status_code=400,
                    detail=f"Cannot set total seats for {type_name} to {new_total_seats} (already booked: {stat.booked_seats})"
                )
            stat.total_seats = new_total_seats
            stat.available_seats = new_total_seats - stat.booked_seats
        else:
            ticket_class_statistics_id = await generate_next_id(db)
            new_stat = TicketClassStatistics(
                ticket_class_statistics_id=ticket_class_statistics_id,
                flight_id=flight.flight_id,
                ticket_class_id=ticket_class.ticket_class_id,
                total_seats=new_total_seats,
                available_seats=new_total_seats,
                booked_seats=0
            )
            db.add(new_stat)

    # Tạo price_map
    price_map = {
        (tp.flight_route_id, tp.ticket_class_id): tp.price
        for tp in ticket_prices
    }

    # Commit
    await db.commit()

    # Truy xuất lại flight
    result = await db.execute(
        select(Flight)
        .where(Flight.flight_id == flight.flight_id)
        .options(
            selectinload(Flight.flight_route).selectinload(FlightRoute.departure_airport),
            selectinload(Flight.flight_route).selectinload(FlightRoute.arrival_airport),
            selectinload(Flight.flight_route).selectinload(FlightRoute.flight_details).selectinload(FlightDetail.transit_airport),
            selectinload(Flight.ticket_class_statistics).selectinload(TicketClassStatistics.ticket_class).selectinload(TicketClass.ticket_prices)
        )
    )
    refreshed_flight = result.unique().scalars().first()
    return refreshed_flight, price_map

    
    
    
async def delete_flight(flight_ids: List[str], db: AsyncSession) -> Optional[Flight]:
    try :
        result = await db.execute(select(Flight).where(Flight.flight_id.in_(flight_ids)))
        flights = result.scalars().all()
        
        if not flights:
            raise HTTPException(status_code= 404, detail= "Flights not exist")
        
        for flight in flights:
            await db.delete(flight)
            
        await db.commit()
        
        return "Delete Successfully"
    
    except SQLAlchemyError as e:
        await db.rollback()
        return f"Delete Failed: {str(e)}"
    
    
    
async def get_ticket_class_by_route(db: AsyncSession,flight_route_id: str, skip: int = 0, limit: int = 1000) -> List[TicketPrice]:
    result = await db.execute(select(TicketPrice)
                            .options( selectinload(TicketPrice.ticket_class))
                            .where(TicketPrice.flight_route_id == flight_route_id).offset(skip).limit(limit))
    return result.unique().scalars().all()
