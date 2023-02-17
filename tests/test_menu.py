from conftest import *
from database.models import Menu
import uuid

router = '/api/v1/menus'
router_id = 'api/v1/menus/{id}'


# Тестовый сценарий: Исходное состояние -> БД пустая.
# 1. Вывод пустого списка меню. 2. Создание меню. 
# 3. Вывод списка меню. 4. Получение меню по id.
# 5. Получение меню по несуществующему id. 
# 6. Изменеие меню
# 7. Удаление меню. 

def test_get_empty_menu_list(client):
    resp = client.get(router)
    assert resp.status_code == 200
    assert resp.json() == []
    

def test_create_menu(client, session_test):
    resp = client.post(
        router,
        json={'title': 'My menu', 'description': 'My menu description'},
    )
    assert resp.status_code == 201
    id = resp.json()["id"]
    menu = session_test.query(Menu).\
        filter(Menu.id == id).first()
    assert resp.json() == menu_to_dict(menu)


def test_get_menu_list(client, session_test):
    resp = client.get(router)
    assert resp.status_code == 200
    menu_list = session_test.query(Menu).all()
    assert resp.json() == [menu_to_dict(menu) for menu in menu_list]
    

def test_get_menu_by_id(client, session_test):
    menu = session_test.query(Menu).one()
    id = menu.id
    resp = client.get(
        router_id.format(id=id),
    )
    assert resp.status_code == 200
    assert resp.json() == menu_to_dict(menu)


def test_menu_not_found(client):
    test_id = uuid.uuid4()
    resp = client.get(
        router_id.format(id=test_id),
    )
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'menu not found'}


def test_update_menu(client, session_test):
    menu = session_test.query(Menu).one()
    id = menu.id
    resp = client.patch(
        router_id.format(id=id),
        json={
            'title': 'My updated menu',
            'description': 'My updated menu description',
        },
    )
    assert resp.status_code == 200
    assert resp.json() == menu_to_dict(menu)


def test_delete_menu(client, session_test):
    menu = session_test.query(Menu).one()
    id = menu.id
    resp = client.delete(
        router_id.format(id=id),
    )
    assert resp.status_code == 200
    assert resp.json() == {
        'status': True,
        'message': 'The menu has been deleted',
     }





