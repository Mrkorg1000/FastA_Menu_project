import asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings
from main import app
# from pytest import fixture
from pytest_asyncio import fixture
from database.db import get_session
from database.models import Base, Menu, Submenu, Dish
from fastapi.testclient import TestClient
from collections.abc import AsyncGenerator

router = '/api/v1/menus'
router_for_sub = '/api/v1/menus/{menu_id}/submenus/'

SQLALCHEMY_TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.db_user_test}:{settings.db_pass_test}@{settings.db_host_test}:{settings.db_port_test}/{settings.db_name_test}"
)

engine_test = create_async_engine(
    SQLALCHEMY_TEST_DATABASE_URL, echo=True, pool_pre_ping=True
)

async_session_test_maker = sessionmaker(bind=engine_test, class_=AsyncSession,
                                   expire_on_commit=False)


@fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@fixture
async def async_session_test() -> AsyncGenerator:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
        async with async_session_test_maker(bind=conn) as session_test:
            yield session_test
            await session_test.flush()
            await session_test.rollback()
        
           
@fixture
async def client(async_session_test):
    def override_get_session():
        return async_session_test
    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@fixture
async def test_menu(async_session_test):
    menu = Menu(
        title = "My test menu",
        description = "Test menu description"
    )
    async_session_test.add(menu)
    await async_session_test.commit()
    await async_session_test.refresh(menu)
    return menu


@fixture
async def test_submenu(async_session_test, test_menu):
    submenu = Submenu(
        title="My test submenu",
        description="Test submenu description",
        menu_id = test_menu.id
    )
    async_session_test.add(submenu)
    await async_session_test.commit()
    await async_session_test.refresh(submenu)
    return submenu


def menu_to_dict(menu: Menu):
    return {
        'id': str(menu.id),
        'title': str(menu.title),
        'description': str(menu.description),
        'submenus_count': menu.submenus_count,
        'dishes_count': menu.dishes_count,
    }


def submenu_to_dict(submenu: Submenu):
    return {
        'id': str(submenu.id),
        'title': str(submenu.title),
        'description': str(submenu.description),
        'dishes_count': submenu.dishes_count,
    }


def dish_to_dict(dish: Dish):
    return {
        'id': str(dish.id),
        'title': str(dish.title),
        'description': str(dish.description),
        'price': float(dish.price),
    }
