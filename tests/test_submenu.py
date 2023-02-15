from conftest import *
from database.models import Submenu
import uuid


router = '/api/v1/menus/{menu_id}/submenus'
router_id = 'api/v1/menus/{menu_id}/submenus/{id}'


# Тестовый сценарий: Исходное состояние -> БД пустая.
# 1. Вывод пустого списка подменю. 2. Создание подменю.
# 3. Вывод списка подменю. 4. Получение подменю по id.
# 5. Получение подменю по несуществующему id.
# 6. Изменеие подменю
# 7. Удаление подменю.

def test_get_empty_submenu_list(client, create_menu_id):
    resp = client.get(router.format(menu_id=create_menu_id))
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_submenu(client, session_test, menu_id_from_db):
    resp = client.post(
        router.format(menu_id=menu_id_from_db),
        json={'title': 'My submenu', 'description': 'My submenu description'},
    )
    assert resp.status_code == 201
    id = resp.json()["id"]
    submenu = get_submenu_by_id(session_test, id)
    assert resp.json() == submenu_to_dict(submenu)


def test_get_submenu_list(client, session_test, menu_id_from_db):
    resp = client.get(router.format(menu_id=menu_id_from_db))
    assert resp.status_code == 200
    submenu_list = session_test.query(Submenu).all()
    assert resp.json() == [submenu_to_dict(submenu) for submenu in submenu_list]


def test_get_submenu_by_id(client, session_test, menu_id_from_db):
    submenu = session_test.query(Submenu).one()
    submenu_id = submenu.id
    resp = client.get(
        router_id.format(menu_id=menu_id_from_db, id=submenu_id)
    )
    assert resp.status_code == 200
    assert resp.json() == submenu_to_dict(submenu)


def test_submenu_not_found(client, session_test, menu_id_from_db):
    # menu_id = get_menu_id_from_db(session_test)
    test_id = uuid.uuid4()
    resp = client.get(
        router_id.format(menu_id=menu_id_from_db, id=test_id)
    )
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'submenu not found'}


def test_update_submenu(client, session_test, menu_id_from_db):
    submenu = session_test.query(Submenu).one()
    submenu_id = submenu.id
    resp = client.patch(
        router_id.format(menu_id=menu_id_from_db, id=submenu_id),
        json={
            'title': 'My updated submenu',
            'description': 'My updated submenu description',
        },
    )
    assert resp.status_code == 200
    assert resp.json() == submenu_to_dict(submenu)


def test_delete_submenu(client, session_test, menu_id_from_db):
    submenu = session_test.query(Submenu).one()
    submenu_id = submenu.id
    resp = client.delete(
        router_id.format(menu_id=menu_id_from_db, id=submenu_id)
    )
    assert resp.status_code == 200
    assert resp.json() == {
        'status': True,
        'message': 'The submenu has been deleted',
    }
