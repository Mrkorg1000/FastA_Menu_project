from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from main import app
from pytest import fixture
from database.db import get_session
from database.models import Base, Menu, Submenu, Dish
from fastapi.testclient import TestClient
router = '/api/v1/menus'
router_for_sub = '/api/v1/menus/{menu_id}/submenus/'

SQLALCHEMY_TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.db_user_test}:{settings.db_pass_test}@{settings.db_host_test}:{settings.db_port_test}/{settings.db_name_test}"
)

engine_test = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, echo=True
)

SessionTest = sessionmaker(bind=engine_test, expire_on_commit=False)


@fixture(scope="module")
def session_test():
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    try:
        session = SessionTest()
        yield session
    finally:
        session.close()
        
           
@fixture(scope="module")
def client(session_test):
    def override_get_session():
        return session_test
    app.dependency_overrides[get_session] = override_get_session
    client = TestClient(app)
    return client


@fixture(scope="module")
def test_menu(session_test):
    menu = Menu(
        title = "My test menu",
        description = "Test menu description"
    )
    session_test.add(menu)
    session_test.commit()
    session_test.refresh(menu)
    return menu


@fixture(scope="module")
def test_submenu(session_test, test_menu):
    submenu = Submenu(
        title="My test submenu",
        description="Test submenu description",
        menu_id = test_menu.id
    )
    session_test.add(submenu)
    session_test.commit()
    session_test.refresh(submenu)
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
        'price': str(dish.price),
    }
