from fastapi import FastAPI, HTTPException , Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.Employee import EmployeeCreate, EmployeeUpdate, EmployeeInDB
from typing import List
from app.deps import get_db
from app.crud.employee import get_all, get_by_id, create, update, remove
from fastapi import Body


router = APIRouter()



@router.get("/", response_model= List[EmployeeInDB])
async def get_all_accounts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    try:
        result = await get_all(db, skip=skip, limit=limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@router.get("/{employee_id}", response_model= EmployeeInDB)
async def find_employee_id(employee_id: str, db : AsyncSession = Depends(get_db)):
    db_obj = await get_by_id(db, employee_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_obj

@router.post("/", response_model=EmployeeInDB)
async def create_employee(
    db: AsyncSession = Depends(get_db),
    obj_in: EmployeeCreate = Body(...)
):
    return await create(db, obj_in)


@router.put("/{employee_id}", response_model= EmployeeInDB)
async def update_info(employee_id: str, obj_in : EmployeeUpdate,db: AsyncSession = Depends(get_db)):
    db_obj = await get_by_id(db, employee_id)
    
    if not db_obj:
        raise HTTPException(status_code= 404, detail= "Employee not found")
    
    return await update(db, db_obj, obj_in)

@router.delete("/{employee_id}", response_model= EmployeeInDB)
async def delete_employee(employee_id: str,db: AsyncSession = Depends(get_db)):
    db_obj = await get_by_id(db, employee_id)
    
    if not db_obj:
        raise HTTPException(status_code= 404, detail= "Employee not found")
    
    return await remove(db, employee_id)
