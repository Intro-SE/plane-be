from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.functions.regulations import get_rules, update_rules
from app.deps import get_db
from fastapi import APIRouter, HTTPException, Depends
from app.functions.regulations import RulesOut, RulesUpdate,FlightTransitOut, get_transit_airport,create_transit, delete_transit, DeleteDetail, create_tkclass, get_ticket_class
from app.functions.regulations import TicketClassCreate, TicketClassRoute, get_ticket_class_by_route, create_ticket_class_by_route

from app.models.TicketClass import TicketClass

router = APIRouter()


@router.get("/regulations", response_model=RulesOut)
async def get_all_rules(db: AsyncSession = Depends(get_db)):
    try:
        rules = await get_rules(db)
        return rules
    except Exception as e:
        raise HTTPException(status_code= 500, detail=str(e))
    
    
@router.put("/update_rule", response_model= RulesOut)
async def update_rule(rules_update: RulesUpdate, db: AsyncSession = Depends(get_db)):
    try:
        new_rules = await update_rules(rules_update,db)
        return new_rules
    except Exception as e:
        raise HTTPException(status_code= 500, detail=str(e))
    
    
    

    
@router.get("/flight_detail", response_model= List[FlightTransitOut])
async def get_all_transit(db: AsyncSession = Depends(get_db)):
    try:
        result = await get_transit_airport(db)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))
    
    
@router.post("/create_transit_airport", response_model= FlightTransitOut)
async def create_transit_airport(input: FlightTransitOut, db: AsyncSession = Depends(get_db)):
    try:
        result = await create_transit(input, db)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))
    
    
@router.delete("/delete_transit_airport", response_model= str)
async def delete_transit_airport(input: DeleteDetail, db: AsyncSession = Depends(get_db)):
    try:
        result = await delete_transit(input, db)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))
    
    
    
@router.get("/get_ticket_class", response_model= List[TicketClassCreate])
async def get_all_ticket_class(db:AsyncSession = Depends(get_db)):
    try:
        result = await get_ticket_class(db)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))
    
    
    
    
@router.post("/create_ticket_class", response_model= TicketClassCreate)
async def create_ticket_class(input: TicketClassCreate, db: AsyncSession = Depends(get_db)):
    try:
        result = await create_tkclass(input, db)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))
    
    
    
@router.get("/ticket_class_by_route", response_model= List[TicketClassRoute])
async def get_ticket_class_route(db: AsyncSession = Depends(get_db)):
    try:
        result = await get_ticket_class_by_route(db)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail= str(e))
    
    
@router.post("/create_ticket_class_by_route", response_model=TicketClassRoute)
async def create_ticket_class_route(input: TicketClassRoute, db: AsyncSession = Depends(get_db)):
    try:
        result = await create_ticket_class_by_route(input, db)
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        tb_str = traceback.format_exc()
        print("Exception traceback:", tb_str)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
