from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class SchemaBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class SchemasMenu(SchemaBase):
    id: int
    submenus_count: int
    dishes_count: int


class SchemasSubMenu(SchemaBase):
    id: int
    dishes_count: int


class SchemasDish(SchemaBase):
    id: int
    price: float


class SchemasCreateUpdateDish(SchemaBase):
    price: float
