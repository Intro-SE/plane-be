from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.functions.regulations import get_rules, update_rules
from app.models.Rules import Rules
from app.deps import get_db
from fastapi import APIRouter, HTTPException, Depends
from app.functions.regulations import RulesOut, RulesUpdate


router = APIRouter()


@router.get("/regulations", response_model=RulesOut)
async def get_all_rules(db: AsyncSession = Depends(get_db)):
    try:
        rules = await get_rules(db)
        return rules
    except Exception as e:
        raise HTTPException(status_code= 500, detail=str(e))
    
    
@router.put("/update", response_model= RulesOut)
async def update(rules_update: RulesUpdate, db: AsyncSession = Depends(get_db)):
    try:
        new_rules = await update_rules(rules_update,db)
        return new_rules
    except Exception as e:
        raise HTTPException(status_code= 500, detail=str(e))
    