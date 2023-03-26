from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Float, func, select, Date, and_
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.dialects.mysql import FLOAT
from sqlalchemy.orm import declarative_base, relationship, MapperProperty, column_property
from datetime import date

Base = declarative_base()


class Price(Base):
    __tablename__ = 'price'
    id = Column(Integer, primary_key=True, autoincrement=True)
    dish_price = Column(Float, nullable=False)
    validity_start = Column(Date, nullable=False)
    validity_end = Column(Date, nullable=False)
    dish_id = Column(
        Integer,
        ForeignKey("dish.id", ondelete="CASCADE")
    )
    dish = relationship(
        'Dish', back_populates='price_values')

class Dish(Base):
    __tablename__ = 'dish'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price: MapperProperty =  column_property(
        select(Price.dish_price)
         .where(Price.dish_id == id)
         .filter(and_(date.today() < Price.validity_end,
                       date.today() > Price.validity_end))
         .correlate_except(Price)
         .scalar_subquery()
    )
    submenu_id = Column(
        Integer,
        ForeignKey("submenu.id", ondelete="CASCADE")
    )
    submenu = relationship(
        'Submenu', back_populates='dishes')
    
    price_values = relationship(
        'Price', cascade="all, delete",
        back_populates='dish'
        )
    


class Submenu(Base):
    __tablename__ = 'submenu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    menu_id = Column(
        Integer,
        ForeignKey("menu.id", ondelete="CASCADE")
    )
    
    dishes_count: MapperProperty =  column_property(
        select(func.count(Dish.id))
         .where(Dish.submenu_id == id)
         .correlate_except(Dish)
         .scalar_subquery(),
    )

    menu = relationship(
        'Menu', 
        back_populates='submenus'
        )
    dishes = relationship(
        'Dish', cascade="all, delete",
        back_populates='submenu'
        )


class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    submenus_count: MapperProperty = column_property(
        select(func.count(Submenu.id))
        .where(Submenu.menu_id == id)
        .correlate_except(Submenu)
        .scalar_subquery(),
    )
    dishes_count: MapperProperty = column_property(
        select(func.count(Dish.id))
        .join(Submenu, Submenu.menu_id == id)
        .where(Dish.submenu_id == Submenu.id)
        .correlate_except(Submenu)
        .scalar_subquery(),
    )
    submenus = relationship(
        'Submenu', cascade="all, delete", back_populates='menu'
        )
