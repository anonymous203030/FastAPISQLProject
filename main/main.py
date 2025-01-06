import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated

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
