import asyncio

from fastapi import FastAPI, HTTPException
from sqlalchemy import select, func
from passlib.context import CryptContext

from main.database import SessionDep
from main.models import BookModel, setup_database, UserModel
from main.schemas import UserSchema, BookAddSchema, UserRegisterSchema

app = FastAPI(docs_url='/')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.get("/books", tags=['Books'],
         summary='Get all Books'
         )
async def get_books(session: SessionDep, skip: int = 0, limit: int = 10):
    query = select(BookModel).offset(skip).limit(limit)
    result = await session.execute(query)
    books = result.scalars().all()

    if not books:
        raise HTTPException(status_code=404, detail="Книги не найдены")
    return {"books": books, "skip": skip, "limit": limit}


@app.get("/books/{book_id}", tags=["Books", "Book"],
         summary='Get Specific Book By ID'
         )
async def get_book(book_id: int, session: SessionDep):
    query = select(BookModel).where(BookModel.id == book_id)
    result = await session.execute(query)
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books", tags=["Books", "Book"], summary="Add New Book")
async def add_book(data: BookAddSchema, session: SessionDep):
    new_book = BookModel(
        title=data.title,
        author=data.author
    )
    session.add(new_book)
    await session.commit()
    return {'success': True, "message": "Книга Успешно Добавлена"}


@app.put("/update_book/{book_id}", tags=["Books", "Book"], summary="Update Book with specifications")
async def update_book(book_id: int, title: str, author: str, session: SessionDep):
    query = (
        select(BookModel)
        .where(BookModel.id == book_id, BookModel.author == author)
    )
    book = await session.execute(query)
    book = book.scalars().first()

    if book:
        book.title = title
        await session.commit()
        return {"message": "Book updated successfully"}
    else:
        return {"message": "Book not found or author does not match"}


@app.get("/books_count_by_author", tags=["Books"], summary="Books amount by authors")
async def get_books_count_by_author(session: SessionDep):
    # Group books by author and count them
    query = select(BookModel.author, func.count(BookModel.id)).group_by(BookModel.author)
    result = await session.execute(query)

    authors_books_count = []
    for author, count in result.all():
        authors_books_count.append({
            "author": author,
            "books_count": count
        })
    return authors_books_count


@app.get("/users", tags=["Users"], summary="Get All Users")
async def get_users(session: SessionDep, skip: int = 0, limit: int = 10):
    query = select(UserModel).offset(skip).limit(limit)
    result = await session.execute(query)
    users = result.scalars().all()

    if not users:
        raise HTTPException(status_code=404, detail="Книги не найдены")

    return {"users": users, "skip": skip, "limit": limit}


@app.get("/users/{user_id}", tags=["Users", "User"], summary="Get Specific User By ID")
async def get_user_by_id(user_id: int, session: SessionDep):
    query = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/register", tags=["Authentication", "Users", "User"])
async def register(data: UserRegisterSchema, session: SessionDep):
    query = select(UserModel).where(UserModel.email == data.email)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists.")

    hashed_password = pwd_context.hash(data.password)

    new_user = UserModel(
        email=data.email,
        password=hashed_password,
        name=data.name,
        surname=data.surname
    )
    session.add(new_user)
    await session.commit()

    return {"success": True, "message": "The User has been registered."}


@app.post("/login", tags=["Users", "User", "Authentication"], summary="Login to User")
async def login(credentials: UserSchema, session: SessionDep):
    query = select(UserModel).where(UserModel.email == credentials.email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user or not pwd_context.verify(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    return {"success": True, "message": "Авторизация успешна"}


@app.get("/profile", summary="Get User Profile with email", tags=["Users", "User", "Profile"])
async def get_profile(email: str, session: SessionDep, offset: int = 0, limit: int = 10):
    query = select(UserModel).offset(offset).limit(limit).where(UserModel.email == email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User doesn't exist")

    return {
        "email": user.email,
        "name": user.name,
        "surname": user.surname,
        "bio": user.bio,
        "age": user.age,
        "gender": user.gender
    }


async def main():
    await setup_database()
    print("Database and tables created Successfully")


if __name__ == '__main__':
    asyncio.run(main())
