from fastapi import FastAPI, Path, Query, Depends, HTTPException, status
from fastapi_users import FastAPIUsers
from sqlalchemy import insert, column
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker

from auth.auth import auth_backend
from auth.database import User, engine
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
async def create_task(name: str, description: str | None = None, User = Depends(current_user)):
    conn = await engine.connect()
    id_new_task = await conn.execute(
        insert(tasks).values(name=name, description=description, author_id = User.id).returning(tasks.c.id)
    )
    await conn.commit()
    return {"status": "Created task",
            "id": id_new_task.scalar()}

@app.delete("/delete_task/{id}")
async def delete_task(id: int, User = Depends(current_user)):
    conn = await engine.connect()
    res = await conn.execute(tasks.select().where((tasks.c.id == id) & (tasks.c.author_id == User.id)))
    try:
        res_obj = res.one()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such task")
    await conn.execute(tasks.delete().where(tasks.c.id == id))
    await conn.commit()
    return {"status": "Deleted task",
            "task_id": id,
            "author_id": User.id}


