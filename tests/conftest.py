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
    f"postgresql://{settings.db_user_test}:{settings.db_pass_test}@{settings.db_host_test}:{settings.db_port_test}/{settings.db_name_test}"
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


@fixture(scope='module')
def create_menu_id(session_test):   # !!!!!!!!!!!!!!!!!!!!!!!!!
    title = 's_menu 1'
    description = 's_menu 1 description'
    menu = Menu(title=title, description=description)
    session_test.add(menu)
    session_test.commit()
    session_test.refresh(menu)
    return menu.id


@fixture(scope='module')
def create_menu_submenu_ids(client, create_menu_id):
    menu_id = create_menu_id
    resp = client.post(router_for_sub.format(
            menu_id=menu_id),
            json={'title': 'My 1submenu', 'description': 'My 1submenu description'},
            )
    submenu_id = resp.json()["id"]
    return menu_id, submenu_id
    
@fixture()
def menu_id_from_db(session_test):
    menu = session_test.query(Menu).first()
    return menu.id


@fixture()
def submenu_id_from_db(session_test):
    submenu = session_test.query(Submenu).first()
    return submenu.id


def get_menu_by_id(session_test, menu_id):
    menu = session_test.query(Menu).filter(Menu.id == menu_id).first()
    return menu


def get_submenu_by_id(session_test, submenu_id):
    submenu = session_test.query(Submenu).filter(Submenu.id == submenu_id).first()
    return submenu


def get_dish_by_id(session_test, dish_id):
    dish = session_test.query(Dish).filter(Dish.id == dish_id).first()
    return dish

    

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

        


