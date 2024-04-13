from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import asyncio
from contextlib import asynccontextmanager

DATABASE_URL = "postgresql+asyncpg://hackathon-user-03:M5nOpQ6rSt@10.28.51.4:5434/hackathon-user-03"

engine = create_async_engine(DATABASE_URL, echo=True)

@asynccontextmanager
async def get_session():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)()
    try:
        yield session
        await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()

def get_connection():
    return engine.connect()

async def execute_query(query):
    query = text(query)
    async with get_connection() as conn:
        async with conn.begin():
            result = await conn.execute(query)
            return await result.fetchall() if result.returns_rows else None
