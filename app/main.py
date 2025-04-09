from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import get_db

app = FastAPI()

@app.get("/")
async def test_db_connection(db: AsyncSession = Depends(get_db)):
    return {"message": "Connected to DB successfully!"}
