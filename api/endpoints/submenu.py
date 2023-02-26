from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import update
from sqlalchemy.orm import Session
from typing import List
from database.db import get_session
from database.models import Menu, Submenu
from api.schemas import SchemaBase, SchemasSubMenu
from uuid import UUID

router = APIRouter()


@router.get("/", response_model=List[SchemasSubMenu])
def get_submenus(session: Session = Depends(get_session)):
    submenus = session.query(Submenu).all()
    return submenus


@router.post("/", response_model=SchemasSubMenu, status_code=status.HTTP_201_CREATED)
def create_submenu(
    menu_id: UUID, submenu: SchemaBase, session: Session = Depends(get_session)
    ):
    new_submenu = Submenu(**submenu.dict())
    new_submenu.menu_id = menu_id
    session.add(new_submenu)
    session.commit()
    session.refresh(new_submenu)

    return new_submenu


@router.get("/{id}", response_model=SchemasSubMenu)
def get_single_submenu(id: UUID, session: Session = Depends(get_session)):
    single_submenu = session.query(Submenu).filter(Submenu.id == id).first()
    if not single_submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="submenu not found"
                            )
    return single_submenu


@router.patch("/{id}", response_model=SchemasSubMenu)
def update_submenu(id: UUID, submenu: SchemaBase,
                session: Session = Depends(get_session)):
    query = session.query(Submenu).filter(Submenu.id == id)

    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="submenu not found"
                            )
    query.update(submenu.dict(exclude_unset=True))
    session.commit()
    updated_submenu = query.first()
    session.refresh(updated_submenu)
    
    return updated_submenu


@router.delete("/{id}")
def delete_single_submenu(id: UUID, session: Session = Depends(get_session)):
    single_submenu = session.query(Submenu).filter(Submenu.id == id).first()
    if not single_submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="submenu not found"
                            )
    session.delete(single_submenu)
    session.commit()
    
    return {"status": True, "message": "The submenu has been deleted"}
