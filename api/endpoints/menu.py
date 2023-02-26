from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import update
from sqlalchemy.orm import Session
from typing import List
from database.db import get_session
from database.models import Menu
from api.schemas import SchemaBase, SchemasMenu
from uuid import UUID

router = APIRouter()


@router.get("/", response_model=List[SchemasMenu])
def get_menus(session: Session = Depends(get_session)):
    menus = session.query(Menu).all()
    return menus


@router.post("/", response_model=SchemasMenu, status_code=status.HTTP_201_CREATED)
def create_menu(menu: SchemaBase, session: Session = Depends(get_session)):
    new_menu = Menu(**menu.dict())
    session.add(new_menu)
    session.commit()
    session.refresh(new_menu)
    return new_menu


@router.get("/{id}", response_model=SchemasMenu)
def get_single_menu(id: UUID, session: Session = Depends(get_session)):
    single_menu = session.query(Menu).filter(Menu.id == id).first()
    if not single_menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="menu not found"
                            )
    return single_menu


@router.patch("/{id}", response_model=SchemasMenu)
def update_menu(id: UUID, menu: SchemaBase,
                    session: Session = Depends(get_session)):
    query = session.query(Menu).filter(Menu.id==id)
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="menu not found"
                            )
    query.update(menu.dict(exclude_unset=True))
    session.commit()
    updated_menu = query.first()
    session.refresh(updated_menu)
    
    return updated_menu


@router.delete("/{id}")
def delete_single_menu(id: UUID, session: Session = Depends(get_session)):
    single_menu = session.query(Menu).filter(Menu.id == id).first()
    if not single_menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="menu not found"
                            )
    session.delete(single_menu)
    session.commit()

    return {"status": True, "message": "The menu has been deleted"}
