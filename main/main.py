import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import List, Annotated, Literal

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
def read_books():
    return books


@app.get("/books/{book_id}", tags=["Книги", "Книга"],
         summary='Получить Конретную Книгу'
         )
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


class NewBook(BaseModel):
    title: str
    author: str


@app.post("/books")
def create_book(new_book: NewBook):
    books.append({
        "id": len(books) + 1,
        "title": new_book.title,
        "author": new_book.author
    })

    return {'success': True, "message": "Книга Успешно Добавлена"}


# data = {
#     "email": "abc@mail.ru",
#     "bio": None,
#     "age": 12,
# }


class UserSchema(BaseModel):
    email: EmailStr
    password: str = Field(max_length=120)
    model_config = ConfigDict(extra='forbid')


class UserDetailsSchema(UserSchema):
    name: str = Field(min_length=2, max_length=100)
    surname: str = Field(min_length=2, max_length=100)
    bio: str | None = Field(max_length=300)
    age: int | None = Field(ge=0, le=130)
    gender: str = Literal['male', 'female']

    model_config = ConfigDict(extra='forbid')


@app.post("/users", tags=["Пользователи", "Пользователь"])
def add_user(user: UserSchema):
    pass


@app.get("/users", tags=["Пользователи"])
def get_users():
    pass

@app.get("/users/{user_id}", tags=["Пользователи", "Пользователь"])
def get_user_by_id(user_id: int):
    pass