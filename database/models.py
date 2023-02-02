from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.dialects.mysql import FLOAT
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menu'
    id = Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    submenus_count = Column(Integer, default=0)
    dishes_count = Column(Integer, default=0)
    submenus = relationship(
        'Submenu', cascade="all, delete", back_populates='menu'
        )


class Submenu(Base):
    __tablename__ = 'submenu'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    menu_id = Column(
        UUID(as_uuid=True),
        ForeignKey("menu.id", ondelete="CASCADE")
    )
    dishes_count = Column(Integer, default=0)
    menu = relationship(
        'Menu', 
        back_populates='submenus'
        )
    dishes = relationship(
        'Dish', cascade="all, delete",
        back_populates='submenu'
        )


class Dish(Base):
    __tablename__ = 'dish'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float)
    submenu_id = Column(
        UUID(as_uuid=True),
        ForeignKey("submenu.id", ondelete="CASCADE")
    )
    submenu = relationship(
        'Submenu', back_populates='dishes')
