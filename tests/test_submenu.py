from conftest import *
from sqlalchemy import select
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

async def test_get_empty_submenu_list(client, test_menu):
    resp = await client.get(router.format(menu_id=test_menu.id))
    assert resp.status_code == 200
    assert resp.json() == []


async def test_create_submenu(client, async_session_test, test_menu):
    resp = await client.post(
        router.format(menu_id=test_menu.id),
        json={'title': 'My submenu',
              'description': 'My submenu description',
              },    
    )
    assert resp.status_code == 201
    submenu_id = resp.json()["id"]
    submenu = await async_session_test.get(Submenu, submenu_id)
    assert resp.json() == submenu_to_dict(submenu)


async def test_get_submenu_list(client, test_submenu):
    resp = await client.get(router.format(menu_id=test_submenu.menu_id))
    assert resp.status_code == 200
    assert resp.json() == [submenu_to_dict(test_submenu)]


async def test_get_submenu_by_id(client, test_submenu):
    resp = await client.get(
        router_id.format(menu_id=test_submenu.menu_id, id=test_submenu.id)
    )
    assert resp.status_code == 200
    assert resp.json() == submenu_to_dict(test_submenu)


async def test_submenu_not_found(client, test_submenu):
    test_id = uuid.uuid4()
    resp = await client.get(
        router_id.format(menu_id=test_submenu.menu_id, id=test_id)
    )
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'submenu not found'}


async def test_update_submenu(client, async_session_test, test_submenu):
    resp = await client.patch(
        router_id.format(menu_id=test_submenu.menu_id, id=test_submenu.id),
        json={
            'title': 'My updated submenu',
            'description': 'My updated submenu description',
        },
    )
    assert resp.status_code == 200
    updated_submenu = await async_session_test.get(Submenu, test_submenu.id)
    assert resp.json() == submenu_to_dict(updated_submenu)


async def test_delete_submenu(client, async_session_test, test_submenu):
    resp = await client.delete(
        router_id.format(menu_id=test_submenu.menu_id, id=test_submenu.id)
    )
    assert resp.status_code == 200
    deleted_submenu = await async_session_test.get(Submenu, test_submenu.id)
    assert deleted_submenu == None
    assert resp.json() == {
        'status': True,
        'message': 'The submenu has been deleted',
    }
