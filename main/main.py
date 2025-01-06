import asyncio

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select

from main.database import SessionDep
from main.models import BookModel, setup_database
from main.schemas import UserSchema, BookSchema, BookAddSchema

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Асинхронность в Python",
        "author": "Mathew"
    },
    {
        "id": 2,
        "title": "Backend разработка в Python",
        "author": "Artyom"
    }
]


@app.get("/books", tags=['Книги'],
         summary='Получить Все Книги'
         )
async def get_books(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query)
    return result.scalars().all()


@app.get("/books/{book_id}", tags=["Книги", "Книга"],
         summary='Получить Конретную Книгу'
         )
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books")
async def add_book(data: BookAddSchema, session: SessionDep):
    new_book = BookModel(
        title=data.title,
        author=data.author
    )
    session.add(new_book)
    await session.commit()
    return {'success': True, "message": "Книга Успешно Добавлена"}


@app.post("/users", tags=["Пользователи", "Пользователь"])
def add_user(user: UserSchema):
    pass


@app.get("/users", tags=["Пользователи"])
def get_users() -> list[UserSchema]:
    pass


@app.get("/users/{user_id}", tags=["Пользователи", "Пользователь"])
def get_user_by_id(user_id: int):
    pass


async def main():
    await setup_database()
    print("Database and tables created Successfully")


if __name__ == '__main__':
    asyncio.run(main())
