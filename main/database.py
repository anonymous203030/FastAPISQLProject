from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# Create books.db sqlite DB file
engine = create_async_engine("sqlite+aiosqlite:///books.db")

# Create DB session
new_session = async_sessionmaker(bind=engine)


async def get_session() -> AsyncGenerator:
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
