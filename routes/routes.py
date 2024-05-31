from datetime import date
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, validator

from auth.auth import get_current_user
from auth.db import db
from models.models import Date_model, User

task_routers = APIRouter()


@task_routers.post('/create_task')
async def create_task(title: str, description: str, is_favourite: bool | None, icon: int, current_user: Annotated[User, Depends(get_current_user)]):
    query = ('INSERT INTO tasks (title, description, author_id, is_favourite, icon) VALUES (:title, :description, :author_id, :is_favourite, :icon)')
    values = {
        'title': title,
        'description': description,
        'author_id': current_user.id,
        'is_favourite': is_favourite,
        'icon': icon
    }
    await db.execute(query=query, values=values)
    return {'message': 'Task created successfully'}

@task_routers.post('/delete_task/{id}')
async def delete_task(id: int, current_user: Annotated[User, Depends(get_current_user)]):
    query = ('DELETE FROM tasks WHERE id = :id')
    await db.execute(query=query, values={'id': id})
    return {'message': 'Task deleted successfully'}

@task_routers.patch('/done_task/{id}')
async def done_task(id: int, current_user: Annotated[User, Depends(get_current_user)]):
    query = ('UPDATE tasks SET is_done = :done WHERE id = :id')
    await db.execute(query=query, values={'done': True, 'id': current_user.id})
    return {'message': 'Task set to done'}

@task_routers.get('/select_tasks/')
async def select_tasks(current_user: Annotated[User, Depends(get_current_user)]):
    query = 'SELECT * FROM tasks WHERE author_id = :author_id'
    result = await db.fetch_all(query=query, values={'author_id': current_user.id})
    return {"User's tasks": result}

