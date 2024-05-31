from typing import Annotated

from fastapi import FastAPI, Depends

from auth.auth import oauth2_scheme
from auth.db import connect_to_db, close_all_connections
from auth.routes import router
from routes.routes import task_routers

app = FastAPI()
app.include_router(router)
app.include_router(task_routers)


@app.on_event("startup")
async def startup():
    await connect_to_db()


@app.on_event("shutdown")
async def shutdown():
    await close_all_connections()


'''
TODO: todo_obj: (title: str, description: str, author_id: int, is_favourite: bool, icon: int, date: TIMESTAMP, isDone: bool)
TODO: route for making task done (not deleting)
Можно сделать "сделанным", а можно просто удалить 

есть ручка для выбора всех тасок у текущего юзера, есть возможность удалить таску по её айди, а будет еще возможность заменить ее isDone
'''