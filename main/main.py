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


@app.get("/books")
def read_books():
    return books

