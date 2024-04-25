from fastapi import FastAPI, Path, Query, Depends, HTTPException, status
from fastapi_users import FastAPIUsers
from sqlalchemy import insert

from auth.auth import auth_backend
from auth.database import User, create_db_and_tables, engine
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from models.models import tasks

from models.object_models import Task

app = FastAPI()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()

@app.post("/create_task")
async def protected_route(name: str, description: str | None = None, User = Depends(current_user)):
    conn = await engine.connect()
    await conn.execute(insert(tasks).values(name=name, description=description, author_id = User.id))
    await conn.commit()
    return {"status": "ok"}

