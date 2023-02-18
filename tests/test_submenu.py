from conftest import *
from database.models import Submenu, Menu
import uuid


router = '/api/v1/menus/{menu_id}/submenus'
router_id = 'api/v1/menus/{menu_id}/submenus/{id}'


# Тестовый сценарий: Исходное состояние -> БД пустая.
# 1. Вывод пустого списка подменю. 2. Создание подменю.
# 3. Вывод списка подменю. 4. Получение подменю по id.
# 5. Получение подменю по несуществующему id.
# 6. Изменеие подменю
# 7. Удаление подменю.

def test_get_empty_submenu_list(client, test_menu):
    resp = client.get(router.format(menu_id=test_menu.id))
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_submenu(client, session_test, test_menu):
    resp = client.post(
        router.format(menu_id=test_menu.id),
        json={'title': 'My submenu',
              'description': 'My submenu description',
              },    
    )
    assert resp.status_code == 201
    id = resp.json()["id"]
    submenu = session_test.query(Submenu).\
        filter(Submenu.id==id).first()
    assert resp.json() == submenu_to_dict(submenu)


def test_get_submenu_list(client, session_test):
    menu = session_test.query(Menu).one()
    resp = client.get(router.format(menu_id=menu.id))
    assert resp.status_code == 200
    submenu_list = session_test.query(Submenu).all()
    assert resp.json() == [submenu_to_dict(submenu)
                           for submenu in submenu_list]


def test_get_submenu_by_id(client, session_test):
    submenu = session_test.query(Submenu).one()
    submenu_id = submenu.id
    menu_id = submenu.menu_id
    resp = client.get(
        router_id.format(menu_id=menu_id, id=submenu_id)
    )
    assert resp.status_code == 200
    assert resp.json() == submenu_to_dict(submenu)


def test_submenu_not_found(client, session_test):
    submenu = session_test.query(Submenu).one()
    menu_id = submenu.menu_id
    test_id = uuid.uuid4()
    resp = client.get(
        router_id.format(menu_id=menu_id, id=test_id)
    )
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'submenu not found'}


def test_update_submenu(client, session_test):
    submenu = session_test.query(Submenu).one()
    submenu_id = submenu.id
    menu_id = submenu.menu_id
    resp = client.patch(
        router_id.format(menu_id=menu_id, id=submenu_id),
        json={
            'title': 'My updated submenu',
            'description': 'My updated submenu description',
        },
    )
    assert resp.status_code == 200
    updated_submenu = session_test.query(Submenu).\
        filter(Submenu.id == submenu_id).first()
    assert resp.json() == submenu_to_dict(updated_submenu)


def test_delete_submenu(client, session_test):
    submenu = session_test.query(Submenu).one()
    submenu_id = submenu.id
    menu_id = submenu.menu_id
    resp = client.delete(
        router_id.format(menu_id=menu_id, id=submenu_id)
    )
    assert resp.status_code == 200
    deleted_submenu = session_test.query(Submenu).\
        filter(Submenu.id == submenu_id).first()
    assert deleted_submenu == None
    assert resp.json() == {
        'status': True,
        'message': 'The submenu has been deleted',
    }
