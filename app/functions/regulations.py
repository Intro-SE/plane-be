from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.models.Rules import Rules
from sqlalchemy import select
from pydantic import BaseModel
from app.models.FlightDetail import FlightDetail
import re
from app.models.Rules import Rules
from app.crud.airport import get_airport_name
from fastapi import HTTPException
from app.models.TicketClass import TicketClass
from sqlalchemy import func, select, join,and_, or_
from sqlalchemy.orm import selectinload
from app.models.TicketPrice import TicketPrice
from app.models.Airport import Airport
from sqlalchemy.orm import selectinload

# Các chỉ số thay đổi quy định
# Get Rules:
class RulesOut(BaseModel):
    airport_number: Optional[int] = None
    min_flight_duration: Optional[int] = None
    max_stop_number: Optional[int] = None
    min_stop_duration: Optional[int] = None
    max_stop_duration: Optional[int] = None
    latest_time_to_book: Optional[int] = None
    latest_time_to_cancel: Optional[int] = None
    ticket_class_number: Optional[int] = None
    
# Update Rules
class RulesUpdate(BaseModel):
    airport_number: Optional[int] = None
    min_flight_duration: Optional[int] = None
    max_stop_number: Optional[int] = None
    min_stop_duration: Optional[int] = None
    max_stop_duration: Optional[int] = None
    latest_time_to_book: Optional[int] = None
    latest_time_to_cancel: Optional[int] = None
    ticket_class_number: Optional[int] = None


# Lấy rule và cập nhật rule    
async def get_rules(db: AsyncSession)-> Optional[RulesOut]:
    query = (select(Rules))
    
    result = await db.execute(query)
    
    rules = result.scalar()
    
    
    return RulesOut(
        airport_number= rules.max_airports,
        min_flight_duration= rules.min_flight_time,
        max_stop_number= rules.max_transit_airports,
        min_stop_duration= rules.min_stop_time,
        max_stop_duration= rules.max_stop_time,
        latest_time_to_book= rules.latest_booking_time,
        latest_time_to_cancel= rules.latest_cancel_time,
        ticket_class_number= rules.ticket_class_count
    )
    

async def update_rules(rules_input: RulesUpdate, db: AsyncSession) -> Optional[RulesOut]:
    query = (select(Rules))
    
    result = await db.execute(query)
    
    rules: Optional[Rules] = result.scalar_one_or_none()

    if rules is None:
        return None

    field_map = {
        "airport_number": "max_airports",
        "min_flight_duration": "min_flight_time",
        "max_stop_number": "max_transit_airports",
        "min_stop_duration": "min_stop_time",
        "max_stop_duration": "max_stop_time",
        "latest_time_to_book": "latest_booking_time",
        "latest_time_to_cancel": "latest_cancel_time",
        "ticket_class_number": "ticket_class_count"
    }

    for pydantic_field, orm_field in field_map.items():
        value = getattr(rules_input, pydantic_field)
        if value is not None:
            setattr(rules, orm_field, value)

    await db.commit()
    await db.refresh(rules)

    return RulesOut(
        airport_number=rules.max_airports,
        min_flight_duration=rules.min_flight_time,
        max_stop_number=rules.max_transit_airports,
        min_stop_duration=rules.min_stop_time,
        max_stop_duration=rules.max_stop_time,
        latest_time_to_book=rules.latest_booking_time,
        latest_time_to_cancel=rules.latest_cancel_time,
        ticket_class_number=rules.ticket_class_count
    )


# Thêm, xóa, sửa thông tin sân bay trunng gian
#### Cập nhật thông tin sân bay trung gian (Có xóa)
# Output trả về cho người dùng
class FlightTransitOut(BaseModel):
    flight_detail_id: Optional[str] = None
    flight_route_id: Optional[str] = None
    transit_airport_name:Optional[str] = None
    stop_time: Optional[int] = None
    note: Optional[str] = None

# Class nhập thông tin thêm sân bay trung gian
class FlightTransitCreate(BaseModel):
    flight_route_id: str
    transit_airport_name: str
    stop_time: int
    note: Optional[str] = None

class DeleteDetail(BaseModel):
    flight_route_id: Optional[str] = None
    transit_airport_name: Optional[str] = None

### Lấy thông tin sân bay trung gian
async def get_transit_airport(db: AsyncSession) -> List[FlightTransitOut]:
    
    flight_detail = await db.execute(select(FlightDetail).options(selectinload(FlightDetail.transit_airport)))
    
    flight_details = flight_detail.scalars().all()
    result = []
    for fl in flight_details:
        result.append(FlightTransitOut(
            flight_detail_id=fl.flight_detail_id,
            flight_route_id= fl.flight_route_id,
            transit_airport_name= fl.transit_airport.airport_name,
            stop_time= fl.stop_time,
            note= fl.note
        ))
    
    return result

##### Tạo sân bay trung gian mới
async def generate_next_id(session):
    result = await session.execute(select(FlightDetail.flight_detail_id))
    ids = [row[0] for row in result.all()]

    max_num = 0
    for bid in ids:
        match = re.search(r'CTCB(\d+)', bid)
        if match:
            num = int(match.group(1))
            max_num = max(max_num, num)

    next_num = max_num + 1
    return f"CTCB{next_num:02d}" 


async def create_transit(input: FlightTransitCreate, db: AsyncSession) -> FlightTransitOut:
    # Lấy quy định hệ thống (giới hạn số sân bay trung gian, thời gian dừng)
    rules_result = await db.execute(select(Rules))
    rules = rules_result.scalar()

    # Đếm số sân bay trung gian hiện tại trong tuyến bay này
    count_result = await db.execute(
        select(func.count(FlightDetail.flight_detail_id))
        .where(FlightDetail.flight_route_id == input.flight_route_id)
    )
    count_ = count_result.scalar()

    # Tạo flight_detail_id mới theo format CTCBxxx
    flight_detail_id = await generate_next_id(db)

    # Kiểm tra tên sân bay có tồn tại không
    transit_airport = await get_airport_name(db, input.transit_airport_name)
    if not transit_airport:
        raise HTTPException(status_code=404, detail=f"Airport '{input.transit_airport_name}' not exists")

    # Kiểm tra quy định về số lượng sân bay trung gian và thời gian dừng
    if count_ >= rules.max_transit_airports:
        raise HTTPException(status_code=400, detail="Số lượng sân bay trung gian vượt quá giới hạn quy định")
    if not (rules.min_stop_time <= input.stop_time <= rules.max_stop_time):
        raise HTTPException(status_code=400, detail="Thời gian dừng không hợp lệ")

    # Tạo bản ghi mới cho sân bay trung gian
    new_transit = FlightDetail(
        flight_detail_id=flight_detail_id,
        flight_route_id=input.flight_route_id,
        transit_airport_id=transit_airport.airport_id,
        stop_time=input.stop_time,
        note=input.note
    )

    # Lưu vào cơ sở dữ liệu
    db.add(new_transit)
    await db.commit()
    await db.refresh(new_transit)

    # Trả về kết quả dưới dạng FlightTransitOut
    return FlightTransitOut(
        flight_detail_id=new_transit.flight_detail_id,
        flight_route_id=new_transit.flight_route_id,
        transit_airport_name=input.transit_airport_name,
        stop_time=new_transit.stop_time,
        note=new_transit.note
    )

####### Xóa sân bay trung gian    
async def delete_transit(input: DeleteDetail, db: AsyncSession) -> str:
    
    transit = await db.execute(select(FlightDetail).options(selectinload(FlightDetail.transit_airport)).where(and_(
        FlightDetail.flight_route_id == input.flight_route_id,
        FlightDetail.transit_airport.has(airport_name=input.transit_airport_name)
    )))
    
    transit_airport = transit.scalar()
    if not transit_airport:
        raise HTTPException(status_code=404, detail="Transit airport not found")

    await db.delete(transit_airport)
    await db.commit()
    return "Deleted successfully"

# Cập nhật sân bay trung gian dựa vào flight_detail_id
async def get_airport_name(db: AsyncSession, name: str) -> Optional[Airport]:
    result = await db.execute(
        select(Airport).where(Airport.airport_name == name)
    )
    return result.scalar_one_or_none()

async def update_transit(input: FlightTransitOut, db: AsyncSession) -> FlightTransitOut:
    # Kiểm tra xem có flight_detail_id không
    if not input.flight_detail_id:
        raise HTTPException(status_code=400, detail="flight_detail_id is required for update")

    # Truy vấn bản ghi chi tiết chuyến bay trung gian cần cập nhật
    transit = await db.execute(
        select(FlightDetail)
        .options(selectinload(FlightDetail.transit_airport))
        .where(FlightDetail.flight_detail_id == input.flight_detail_id)
    )
    transit_detail = transit.scalar_one_or_none()

    if not transit_detail:
        raise HTTPException(status_code=404, detail="Transit airport detail not found")

    # Lấy quy định về thời gian dừng
    rules = (await db.execute(select(Rules))).scalar_one_or_none()
    if not rules:
        raise HTTPException(status_code=500, detail="Rules not found")

    # => Cập nhật các trường nếu người dùng cung cấp

    # Cập nhật mã tuyến bay (optional)
    if input.flight_route_id is not None:
        transit_detail.flight_route_id = input.flight_route_id

    # Cập nhật thời gian dừng
    if input.stop_time is not None:
        if input.stop_time < rules.min_stop_time or input.stop_time > rules.max_stop_time:
            raise HTTPException(
                status_code=400,
                detail=f"Stop time must be between {rules.min_stop_time} and {rules.max_stop_time} minutes"
            )
        transit_detail.stop_time = input.stop_time

    # Cập nhật ghi chú
    if input.note is not None:
        transit_detail.note = input.note

    # Cập nhật tên sân bay trung gian (chuyển thành ID)
    if input.transit_airport_name is not None:
        new_airport = await get_airport_name(db, input.transit_airport_name)
        if not new_airport:
            raise HTTPException(status_code=404, detail="New transit airport not found")
        transit_detail.transit_airport_id = new_airport.airport_id

    # Commit các thay đổi
    await db.commit()
    await db.refresh(transit_detail)

    # Trả về dữ liệu đã cập nhật dưới dạng FlightTransitOut
    return FlightTransitOut(
        flight_detail_id=transit_detail.flight_detail_id,
        flight_route_id=transit_detail.flight_route_id,
        transit_airport_name=transit_detail.transit_airport.airport_name if transit_detail.transit_airport else None,
        stop_time=transit_detail.stop_time,
        note=transit_detail.note
    )

# Thêm, sửa các hạng vé của bảng Hạng vé
### Cập nhật thông tin hạng vé bảng Hạng vé (Không xóa)

class TicketClassOut(BaseModel):
    ticket_class_id: Optional[str] = None
    ticket_class_name: Optional[str] = None

class TicketClassCreate(BaseModel):
    ticket_class_name: Optional[str] = None
   
class TicketClassUpdate(BaseModel):
    ticket_class_id: Optional[str] = None
    ticket_class_name: Optional[str] = None

## Lấy thông tin các hạng vé của bảng Hạng vé
async def get_ticket_class(db: AsyncSession) -> List[TicketClassOut]:
    result = await db.execute(select(TicketClass))
    
    return result.unique().scalars().all()

# Tạo một hạng vé mới trong bảng Hạng vé
async def generate_next_ticket_class_id(session):
    result = await session.execute(select(TicketClass.ticket_class_id))
    ids = [row[0] for row in result.all()]

    max_num = 0
    for bid in ids:
        match = re.search(r'HV(\d+)', bid)
        if match:
            num = int(match.group(1))
            max_num = max(max_num, num)

    next_num = max_num + 1
    return f"HV{next_num:02d}" 

async def create_tkclass(input: TicketClassCreate, db: AsyncSession) -> Optional[TicketClassOut]:
    # Kiểm tra xem tên hạng vé đã tồn tại chưa (case-sensitive)
    existing_result = await db.execute(
        select(TicketClass).where(TicketClass.ticket_class_name == input.ticket_class_name)
    )
    existing_class = existing_result.unique().scalar_one_or_none()

    if existing_class:
        raise HTTPException(
            status_code=400,
            detail=f"Ticket class with name '{input.ticket_class_name}' already exists."
        )

    # Nếu chưa có thì tạo mới
    ticket_class_id = await generate_next_ticket_class_id(db)
    new_ticket_class = TicketClass(
        ticket_class_id=ticket_class_id,
        ticket_class_name=input.ticket_class_name
    )
    db.add(new_ticket_class)
    await db.commit()
    await db.refresh(new_ticket_class)

    return TicketClassOut(
        ticket_class_id=new_ticket_class.ticket_class_id,
        ticket_class_name=new_ticket_class.ticket_class_name
    )


# Sửa hạng vé trong bảng Hạng vé
async def update_ticket_classs(input: TicketClassUpdate, db: AsyncSession) -> TicketClassOut:
    if not input.ticket_class_id:
        raise HTTPException(status_code=400, detail="ticket_class_id is required")

    # Tìm hạng vé theo ID
    result = await db.execute(
        select(TicketClass).where(TicketClass.ticket_class_id == input.ticket_class_id)
    )
    ticket_class = result.unique().scalar_one_or_none()
    if not ticket_class:
        raise HTTPException(status_code=404, detail="Ticket class not found")

    # Nếu người dùng muốn đổi tên hạng vé, kiểm tra xem tên mới đã tồn tại chưa
    if input.ticket_class_name:
        # Tìm hạng vé khác có tên trùng
        dup_result = await db.execute(
            select(TicketClass)
            .where(
                TicketClass.ticket_class_name == input.ticket_class_name,
                TicketClass.ticket_class_id != input.ticket_class_id  # Loại trừ chính nó
            )
        )
        duplicate = dup_result.unique().scalar_one_or_none()
        if duplicate:
            raise HTTPException(status_code=400, detail=f"Ticket class name '{input.ticket_class_name}' already exists.")

        ticket_class.ticket_class_name = input.ticket_class_name

    await db.commit()
    return TicketClassOut(
        ticket_class_id=ticket_class.ticket_class_id,
        ticket_class_name=ticket_class.ticket_class_name
    )


# Thêm, sửa hạng vé cho các tuyến bay
### Cập nhật thông tin hạng vé Tuyến bay (Không xóa)
class TicketClassRoute(BaseModel):
    ticket_price_id: Optional[str] = None
    flight_route_id: Optional[str] = None
    ticket_class_name: Optional[str] = None
    price: Optional[int] = None

class TicketClassRouteCreate(BaseModel):
    flight_route_id: Optional[str] = None
    ticket_class_name: Optional[str] = None
    price: Optional[int] = None


## Lấy tất cả các hạng vé cho các tuyến bay
async def get_ticket_class_by_route(db: AsyncSession) -> List[TicketClassRoute]:
    result = await db.execute(select(TicketPrice).options(selectinload(TicketPrice.ticket_class)))
    
    results = result.scalars().all()

    ticket_class = []
    
    for result in results:
        ticket_class.append(TicketClassRoute(
            ticket_price_id = result.ticket_price_id,
            flight_route_id= result.flight_route_id,
            ticket_class_name= result.ticket_class.ticket_class_name,
            price = result.price
        ))


    return ticket_class

# Tạo một hạng vé mới cho một tuyến bay
async def generate_ticket_price_id(session) -> str:
    result = await session.execute(select(TicketPrice.ticket_price_id))
    ids = [row[0] for row in result.fetchall() if row[0]]

    max_num = 0
    for bid in ids:
        match = re.search(r'DG(\d+)', bid)
        if match:
            try:
                num = int(match.group(1))
                max_num = max(max_num, num)
            except ValueError:
                continue  

    next_num = max_num + 1
    return f"DG{next_num:02d}" 

async def get_ticket_class_id_by_name(name: str, db: AsyncSession) -> str:
    result = await db.execute(
        select(TicketClass.ticket_class_id)
        .where(TicketClass.ticket_class_name == name)
    )
    ticket_class_id = result.scalar_one_or_none()

    if not ticket_class_id:
        raise HTTPException(status_code=404, detail=f"Ticket class '{name}' not exists.")

    return ticket_class_id

async def create_ticket_class_by_route(input: TicketClassRouteCreate, db: AsyncSession) -> TicketClassRoute:
    # 1. Lấy quy định hệ thống (số lượng hạng vé tối đa mỗi tuyến bay)
    rules_result = await db.execute(select(Rules))
    rules = rules_result.scalar_one_or_none()  
    if not rules:
        raise HTTPException(status_code=404, detail="Rules not found")

    # 2. Đếm số hạng vé hiện có trong tuyến bay này
    count_result = await db.execute(
        select(func.count(TicketPrice.ticket_class_id))
        .where(TicketPrice.flight_route_id == input.flight_route_id)
    )
    current_ticket_class_count = count_result.scalar()

    # print(current_ticket_class_count)
    # print(rules.ticket_class_count)

    if current_ticket_class_count >= rules.ticket_class_count:
        raise HTTPException(status_code=400, detail="Ticket class count for this route has reached the limit")

    # 3. Tìm ticket_class_id từ tên (nếu không có sẽ raise lỗi)
    ticket_class_id = await get_ticket_class_id_by_name(input.ticket_class_name, db)

    # 4. Kiểm tra xem tuyến bay + hạng vé này đã tồn tại chưa
    existing = await db.execute(
        select(TicketPrice).where(
            TicketPrice.flight_route_id == input.flight_route_id,
            TicketPrice.ticket_class_id == ticket_class_id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Ticket price already exists for this route and class")

    # 5. Sinh ticket_price_id mới
    new_id = await generate_ticket_price_id(db)

    # 6. Tạo đối tượng và lưu vào DB
    new_price = TicketPrice(
        ticket_price_id=new_id,
        flight_route_id=input.flight_route_id,
        ticket_class_id=ticket_class_id,
        price=input.price
    )
    db.add(new_price)
    await db.commit()
    await db.refresh(new_price)

    # 7. Trả về kết quả đúng định dạng
    return TicketClassRoute(
        ticket_price_id=new_price.ticket_price_id,
        flight_route_id=input.flight_route_id,
        ticket_class_name=input.ticket_class_name,
        price=input.price
    )



# Sửa hạng vé cho tuyến bay
async def update_ticket_class_by_route(input: TicketClassRoute, db: AsyncSession) -> TicketClassRoute:
    if not input.ticket_price_id:
        raise HTTPException(status_code=400, detail="ticket_price_id is required")

    # 1. Truy xuất bản ghi TicketPrice theo ID
    result = await db.execute(
        select(TicketPrice).where(TicketPrice.ticket_price_id == input.ticket_price_id)
    )
    ticket_price = result.scalar_one_or_none()
    if not ticket_price:
        raise HTTPException(status_code=404, detail="Ticket price not found")

    # 2. Lấy thông tin ticket_class_id nếu tên mới được cung cấp
    new_ticket_class_id = None
    if input.ticket_class_name:
        class_result = await db.execute(
            select(TicketClass).where(TicketClass.ticket_class_name == input.ticket_class_name)
        )
        ticket_class = class_result.scalars().first()
        if not ticket_class:
            raise HTTPException(status_code=404, detail=f"Ticket class '{input.ticket_class_name}' not found.")
        new_ticket_class_id = ticket_class.ticket_class_id
    else:
        # Nếu không truyền vào tên, ta cần truy vấn ngược để đưa vào output
        class_result = await db.execute(
            select(TicketClass.ticket_class_name).where(
                TicketClass.ticket_class_id == ticket_price.ticket_class_id
            )
        )
        input.ticket_class_name = class_result.scalars().first()

    # 3. Nếu người dùng truyền vào flight_route_id, thì kiểm tra số lượng hạng vé
    if input.flight_route_id:
        route_ticket_count_result = await db.execute(
            select(func.count()).select_from(TicketPrice).where(
                TicketPrice.flight_route_id == input.flight_route_id
            )
        )
        current_count = route_ticket_count_result.scalar()

        rules_result = await db.execute(select(Rules))
        rules = rules_result.scalars().first()
        if not rules:
            raise HTTPException(status_code=500, detail="Rules not found")

        if current_count > rules.ticket_class_count:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot assign ticket to route '{input.flight_route_id}' because it already has {current_count} ticket classes (max: {rules.ticket_class_count})"
            )

        ticket_price.flight_route_id = input.flight_route_id

    # 4. Cập nhật ticket_class_id nếu được truyền
    if new_ticket_class_id:
        ticket_price.ticket_class_id = new_ticket_class_id

    # 4.5. Kiểm tra bộ (flight_route_id, ticket_class_id) đã tồn tại chưa (ngoại trừ bản ghi hiện tại)
    duplicate_check = await db.execute(
        select(TicketPrice).where(
            TicketPrice.flight_route_id == ticket_price.flight_route_id,
            TicketPrice.ticket_class_id == ticket_price.ticket_class_id,
            TicketPrice.ticket_price_id != ticket_price.ticket_price_id  # Tránh chính nó
        )
    )
    if duplicate_check.scalars().first():
        raise HTTPException(
            status_code=400,
            detail=f"A ticket class '{input.ticket_class_name}' already exists for flight route '{ticket_price.flight_route_id}'"
        )

    # 5. Cập nhật giá
    if input.price is not None:
        ticket_price.price = input.price

    # 6. Commit và refresh
    await db.commit()
    await db.refresh(ticket_price)

    # 7. Trả về output
    return TicketClassRoute(
        ticket_price_id=ticket_price.ticket_price_id,
        flight_route_id=ticket_price.flight_route_id,
        ticket_class_name=input.ticket_class_name,
        price=ticket_price.price
    )


