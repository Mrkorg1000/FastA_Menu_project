from conftest import *
from sqlalchemy import select
from database.models import Menu
import uuid

router = '/api/v1/menus'
router_id = 'api/v1/menus/{id}'
pagination_router = '/api/v1/menus/?offset={offset}&limit={limit}'


# Тестовый сценарий: Исходное состояние -> БД пустая.
# 1. Вывод пустого списка меню. 2. Создание меню. 
# 3. Вывод списка меню. 4. Получение меню по id.
# 5. Получение меню по несуществующему id. 
# 6. Изменеие меню
# 7. Удаление меню. 

async def test_get_empty_menu_list(client):
    resp = await client.get(router, follow_redirects=True)
    assert resp.status_code == 200
    assert resp.json() == []
    

async def test_create_menu(client, async_session_test):
    resp = await client.post(
        router,
        json={'title': 'My menu', 'description': 'My menu description'},
        follow_redirects=True
    )
    assert resp.status_code == 201
    menu_id = resp.json()["id"]
    menu = await async_session_test.get(Menu, menu_id)
    assert resp.json() == menu_to_dict(menu)


async def test_get_menu_list(client, test_menu):
    resp = await client.get(router, follow_redirects=True)
    assert resp.status_code == 200
    assert resp.json() == [menu_to_dict(test_menu)]
    

async def test_get_menu_by_id(client, test_menu):
    resp = await client.get(
        router_id.format(id=test_menu.id),
    )
    assert resp.status_code == 200
    assert resp.json() == menu_to_dict(test_menu)


async def test_menu_not_found(client):
    resp = await client.get(
        router_id.format(id=10),
    )
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'menu not found'}

async def test_update_menu(client, async_session_test, test_menu):
    resp = await client.patch(
        router_id.format(id=test_menu.id),
        json={
            'title': 'My updated menu',
            'description': 'My updated menu description',
        },
    )
    assert resp.status_code == 200
    updated_menu = await async_session_test.\
                    get(Menu, test_menu.id)   
    assert resp.json() == menu_to_dict(updated_menu)
    

async def test_delete_menu(client, async_session_test, test_menu):
    resp = await client.delete(
        router_id.format(id=test_menu.id),
    )
    assert resp.status_code == 200
    deleted_menu = await async_session_test.\
                    get(Menu, test_menu.id)
    assert deleted_menu == None
    assert resp.json() == {
        'status': True,
        'message': 'The menu has been deleted',
     }


async def test_menu_pagination_order(client, menus_for_pagination):
    resp = await client.get(
        pagination_router.format(offset=0, limit=10),
        follow_redirects=True
    )
    assert resp.status_code == 200
    assert resp.json() == [menu_to_dict(test_menu) for test_menu in menus_for_pagination[:10]]

    resp = await client.get(
        pagination_router.format(offset=10, limit=10),
        follow_redirects=True
    )
    assert resp.status_code == 200
    assert resp.json() == [menu_to_dict(test_menu) for test_menu in menus_for_pagination[10:]]