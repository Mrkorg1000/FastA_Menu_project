from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database.db import get_session
from database.models import Menu
from api.schemas import SchemaBase, SchemasMenu
from uuid import UUID

router = APIRouter()


@router.get("/", response_model=List[SchemasMenu])
async def get_menus(session: AsyncSession = Depends(get_session)):
    menus = (await session.execute(select(Menu))).scalars().fetchall()
    return menus


@router.post("/", response_model=SchemasMenu, status_code=status.HTTP_201_CREATED)
async def create_menu(menu: SchemaBase, session: AsyncSession = Depends(get_session)):
   
    new_menu = Menu(**menu.dict())
    session.add(new_menu)
    await session.commit()
    await session.refresh(new_menu)
    return new_menu


@router.get("/{id}", response_model=SchemasMenu)  #, response_model=SchemasMenu
async def get_single_menu(id: UUID, session: AsyncSession = Depends(get_session)):
    single_menu = await session.get(Menu, id)
    if not single_menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="menu not found"
                            )
    return single_menu


@router.patch("/{id}", response_model=SchemasMenu)
async def update_menu(id: UUID, menu: SchemaBase,
                    session: AsyncSession = Depends(get_session)):
    db_menu = await session.get(Menu, id)
    if not db_menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="menu not found"
        )
    
    menu_data = menu.dict(exclude_unset=True)
    for key, value in menu_data.items():
        setattr(db_menu, key, value)
    
    await session.commit()
    await session.refresh(db_menu)
    return db_menu


@router.delete("/{id}")
async def delete_single_menu(id: UUID, session: AsyncSession = Depends(get_session)):
    single_menu = await session.get(Menu, id)
    if not single_menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="menu not found"
                            )
    await session.delete(single_menu)
    await session.commit()

    return {"status": True, "message": "The menu has been deleted"}
