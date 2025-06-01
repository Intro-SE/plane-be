from app.models.FlightRoute import FlightRoute
from sqlalchemy import select, func
import re








async def generate_next_id_tb(session):
    result = await session.execute(
        select(func.max(FlightRoute.flight_route_id))
    )
    max_id = result.scalar()

    if not max_id:
        return "TB01"
    
    match = re.search(r'TB(\d+)', max_id)
    if match:
        next_num = int(match.group(1)) + 1
        return f"TB{next_num:02d}" 
