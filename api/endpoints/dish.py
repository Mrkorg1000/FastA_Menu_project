from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import update
from sqlalchemy.orm import Session
from typing import List
from database.db import get_session
from database.models import Menu, Submenu, Dish
from api.schemas import SchemaBase, SchemasDish, SchemasCreateUpdateDish
from uuid import UUID

router = APIRouter()


@router.get("/", response_model=List[SchemasDish])
def get_dishes(session: Session = Depends(get_session)):
    dishes = session.query(Dish).all()
    return dishes


@router.post("/", response_model=SchemasDish, status_code=status.HTTP_201_CREATED)
def create_dish(
    submenu_id: UUID, dish: SchemasCreateUpdateDish,
    session: Session = Depends(get_session)
):
    new_dish = Dish(**dish.dict())
    new_dish.submenu_id = submenu_id
    session.add(new_dish)
    session.commit()
    session.refresh(new_dish)

    return new_dish


@router.get("/{id}", response_model=SchemasDish)
def get_single_dish(id: UUID, session: Session = Depends(get_session)):
    single_dish = session.query(Dish).filter(Dish.id == id).first()
    if not single_dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="dish not found"
                            )
    return single_dish


@router.patch("/{id}", response_model=SchemasDish)
def update_dish(id: UUID, dish: SchemasCreateUpdateDish,
                   session: Session = Depends(get_session)):
    query = session.query(Dish).filter(Dish.id == id)

    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="dish not found"
                            )
    query.update(dish.dict(exclude_unset=True))
    session.commit()
    updated_dish = query.first()
    session.refresh(updated_dish)
    
    return updated_dish


@router.delete("/{id}")
def delete_single_dish(id: UUID, session: Session = Depends(get_session)):
    single_dish = session.query(Dish).filter(Dish.id == id).first()
    if not single_dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="dish not found"
                            )
    session.delete(single_dish)
    session.commit()
    
    return {"status": True, "message": "The dish has been deleted"}
