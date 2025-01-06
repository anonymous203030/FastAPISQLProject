import asyncio

from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from passlib.context import CryptContext

from main.database import SessionDep
from main.models import BookModel, setup_database, UserModel
from main.schemas import UserSchema, BookSchema, BookAddSchema, UserRegisterSchema

app = FastAPI(docs_url='/')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
async def get_book(book_id: int, session: SessionDep):
    query = select(BookModel).where(BookModel.id == book_id)
    result = await session.execute(query)
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


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
async def add_user(user: UserSchema):
    pass


@app.get("/users", tags=["Пользователи"])
async def get_users() -> list[UserSchema]:
    pass


@app.get("/users/{user_id}", tags=["Пользователи", "Пользователь"])
async def get_user_by_id(user_id: int):
    pass


@app.post("/register")
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


@app.post("/login")
async def login(credentials: UserSchema, session: SessionDep):
    query = select(UserModel).where(UserModel.email == credentials.email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user or not pwd_context.verify(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    return {"success": True, "message": "Авторизация успешна"}


@app.get("/profile", summary="Get User Profile with email")
async def get_profile(email: str, session: SessionDep):
    query = select(UserModel).where(UserModel.email == email)
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
