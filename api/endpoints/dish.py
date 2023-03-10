from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database.db import get_session
from database.models import Menu, Submenu, Dish
from api.schemas import SchemaBase, SchemasDish, SchemasCreateUpdateDish
from uuid import UUID

router = APIRouter()


@router.get("/", response_model=List[SchemasDish])
async def get_dishes(session: AsyncSession = Depends(get_session),
                     offset: int=0, limit: int = 2):
    dishes = await session.execute(
        select(Dish).order_by(Dish.id).\
            offset(offset).limit(limit)
    )
    return dishes.scalars().fetchall()


@router.post("/", response_model=SchemasDish, status_code=status.HTTP_201_CREATED)
async def create_dish(
    submenu_id: int, dish: SchemasCreateUpdateDish,
    session: AsyncSession = Depends(get_session)
):
    new_dish = Dish(**dish.dict())
    new_dish.submenu_id = submenu_id
    session.add(new_dish)
    await session.commit()
    await session.refresh(new_dish)

    return new_dish


@router.get("/{id}", response_model=SchemasDish)
async def get_single_dish(id: int, session: AsyncSession = Depends(get_session)):
    single_dish = await session.get(Dish, id)
    if not single_dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="dish not found"
                            )
    return single_dish


@router.patch("/{id}", response_model=SchemasDish)
async def update_dish(id: int, dish: SchemasCreateUpdateDish,
                   session: AsyncSession = Depends(get_session)):
    db_dish = await session.get(Dish, id)

    if not db_dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="dish not found"
                            )
    dish_data = dish.dict(exclude_unset=True)
    for key, value in dish_data.items():
        setattr(db_dish, key, value)
    await session.commit()
    await session.refresh(db_dish)
    
    return db_dish


@router.delete("/{id}")
async def delete_single_dish(id: int, session: AsyncSession = Depends(get_session)):
    single_dish = await session.get(Dish, id)
    if not single_dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="dish not found"
                            )
    await session.delete(single_dish)
    await session.commit()
    
    return {"status": True, "message": "The dish has been deleted"}
