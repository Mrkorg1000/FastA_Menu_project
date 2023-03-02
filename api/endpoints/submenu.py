from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database.db import get_session
from database.models import Menu, Submenu
from api.schemas import SchemaBase, SchemasSubMenu
from uuid import UUID

router = APIRouter()


@router.get("", response_model=List[SchemasSubMenu])
async def get_submenus(session: AsyncSession = Depends(get_session)):
    submenus = await session.execute(select(Submenu))
    return submenus.scalars().fetchall()


@router.post("", response_model=SchemasSubMenu, status_code=status.HTTP_201_CREATED)
async def create_submenu(
    menu_id: UUID, submenu: SchemaBase, session: AsyncSession = Depends(get_session)
    ):
    new_submenu = Submenu(**submenu.dict())
    new_submenu.menu_id = menu_id
    session.add(new_submenu)
    await session.commit()
    await session.refresh(new_submenu)

    return new_submenu


@router.get("/{id}", response_model=SchemasSubMenu)
async def get_single_submenu(id: UUID, session: AsyncSession = Depends(get_session)):
    single_submenu = await session.get(Submenu, id)
    if not single_submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="submenu not found"
                            )
    return single_submenu


@router.patch("/{id}", response_model=SchemasSubMenu)
async def update_submenu(id: UUID, submenu: SchemaBase,
                session: AsyncSession = Depends(get_session)):
    db_submenu = await session.get(Submenu, id)

    if not db_submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="submenu not found"
                            )
    submenu_data = submenu.dict(exclude_unset=True)
    for key, value in submenu_data.items():
        setattr(db_submenu, key, value)
    await session.commit()
    await session.refresh(db_submenu)
    
    return db_submenu


@router.delete("/{id}")
async def delete_single_submenu(id: UUID, session: AsyncSession = Depends(get_session)):
    single_submenu = await session.get(Submenu, id)
    if not single_submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="submenu not found"
                            )
    await session.delete(single_submenu)
    await session.commit()
    
    return {"status": True, "message": "The submenu has been deleted"}
