from app.models.FlightRoute import FlightRoute
from sqlalchemy import select, func
import re
from app.schemas.FlightRoute import FlightRouteInDB, FlightRouteCreate, FlightRouteUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
import re
from typing import Optional, List
from datetime import datetime
from sqlalchemy import func
from fastapi import HTTPException

async def get_id(db: AsyncSession, flight_route_id: str) -> Optional[FlightRoute]:
    result = await db.execute(select(FlightRoute).where(FlightRoute.flight_route_id == flight_route_id))
    
    return result.unique().scalars().one_or_none()

async def get_all_flightroutes(db: AsyncSession, skip : int = 0, limit : int = 0) -> List[FlightRoute]:
    result = await db.execute(select(FlightRoute)
                              .options(
                                selectinload(FlightRoute.departure_airport),
                                selectinload(FlightRoute.arrival_airport),
                                selectinload(FlightRoute.flights),
                                selectinload(FlightRoute.flight_details),
                                selectinload(FlightRoute.ticket_prices),
                              ).offset(skip).limit(limit))
    
    return result.scalars().all()



async def generate_flightroute_id(session):
    result = await session.execute(select(FlightRoute.flight_route_id))
    ids = [row[0] for row in result.all()]

    max_num = 0
    for bid in ids:
        match = re.search(r'TB(\d+)', bid)
        if match:
            num = int(match.group(1))
            max_num = max(max_num, num)

    next_num = max_num + 1
    return f"TB{next_num:02d}" 


async def create_flightroute(db : AsyncSession, flightrouter: FlightRouteCreate) -> FlightRoute:
    # Kiểm tra tuyến bay đã tồn tại (không phân biệt chữ hoa/chữ thường)
    result = await db.execute(
        select(FlightRoute).where(
            func.lower(FlightRoute.departure_airport_id) == flightrouter.departure_airport_id.lower(),
            func.lower(FlightRoute.arrival_airport_id) == flightrouter.arrival_airport_id.lower()
        )
    )
    existing_route = result.scalar_one_or_none()

    if existing_route:
        raise HTTPException(
            status_code=400,
            detail="Flight route with the same departure and arrival airports already exists."
        )

    # Nếu chưa tồn tại, tiến hành tạo
    flight_route_id = await generate_flightroute_id(db)
    new_flightroute = FlightRoute(
        flight_route_id = flight_route_id,
        departure_airport_id = flightrouter.departure_airport_id,
        arrival_airport_id = flightrouter.arrival_airport_id
    )
    db.add(new_flightroute)
    await db.commit()
    await db.refresh(new_flightroute)
    return new_flightroute



async def update_flightroute(db: AsyncSession, db_flightroute: FlightRoute, flight_route_update: FlightRouteUpdate) -> FlightRoute:
    update_data = flight_route_update.dict(exclude_unset=True)

    # Lấy giá trị mới (nếu không cập nhật thì giữ nguyên giá trị cũ)
    departure_id = update_data.get("departure_airport_id", db_flightroute.departure_airport_id)
    arrival_id = update_data.get("arrival_airport_id", db_flightroute.arrival_airport_id)

    # Kiểm tra xem có tuyến bay nào trùng departure và arrival không (trừ chính nó)
    result = await db.execute(
        select(FlightRoute).where(
            func.lower(FlightRoute.departure_airport_id) == departure_id.lower(),
            func.lower(FlightRoute.arrival_airport_id) == arrival_id.lower(),
            FlightRoute.flight_route_id != db_flightroute.flight_route_id  # loại trừ chính tuyến hiện tại
        )
    )
    existing_route = result.scalar_one_or_none()

    # Nếu đã tồn tại tuyến bay trùng thì không cho cập nhật
    if existing_route:
        raise HTTPException(
            status_code=400,
            detail="Flight route with the same departure and arrival airports already exists."
        )

    # Cập nhật dữ liệu
    for key, value in update_data.items():
        setattr(db_flightroute, key, value)

    await db.commit()
    await db.refresh(db_flightroute)
    return db_flightroute

async def delete_flightroute(db: AsyncSession,  obj_in: FlightRoute) -> Optional[FlightRoute]:
    if obj_in:
        await db.delete(obj_in)
        await db.commit()
    return obj_in