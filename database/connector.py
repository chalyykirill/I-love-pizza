import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

DATABASE_URL = "postgresql+asyncpg://hackathon-user-03:M5nOpQ6rSt@10.28.51.4:5434/hackathon-user-03"

engine = create_async_engine(DATABASE_URL, echo=True)

def get_session():
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

def get_connection():
    return engine.connect()

async def execute_query(query):
    query = text(query)
    async with get_connection() as conn:
        async with conn.begin():
            result = await conn.execute(query)
            return await result.fetchall() if result.returns_rows else None
