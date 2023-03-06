from conftest import *
from sqlalchemy import select
from database.models import Menu, Submenu, Dish
import uuid

router = '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes'
router_id = 'api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{id}'

# Тестовый сценарий: Исходное состояние -> БД пустая.
# 1. Вывод пустого списка блюд. 2. Создание блюда.
# 3. Вывод списка блюд. 4. Получение блюда по id.
# 5. Получение блюда по несуществующему id.
# 6. Изменеие блюда
# 7. Удаление блюда.



async def test_get_empty_dish_list(client,   test_submenu):
    resp = await client.get(router.format(menu_id=test_submenu.menu_id, submenu_id=test_submenu.id))
    assert resp.status_code == 200
    assert resp.json() == []


async def test_create_dish(client, async_session_test, test_submenu):
    resp = await client.post(
        router.format(menu_id=test_submenu.menu_id, submenu_id=test_submenu.id),
        json={'title': 'My super dish', 'description': 'My super dish description',
              'price': '12.50',
        },
    )
    assert resp.status_code == 201
    dish_id = resp.json()["id"]
    dish = await async_session_test.get(Dish, dish_id)
    assert resp.json() == dish_to_dict(dish)


async def test_get_dish_list(client, test_submenu, test_dish):
    resp = await client.get(router.format(
        menu_id=test_submenu.menu_id, submenu_id=test_submenu.id)
    )
    assert resp.status_code == 200
    assert resp.json() == [dish_to_dict(test_dish)]


async def test_get_dish_by_id(client, test_submenu, test_dish):
    resp = await client.get(
        router_id.format(menu_id=test_submenu.menu_id, submenu_id=test_submenu.id,
        id=test_dish.id)
    )
    assert resp.status_code == 200
    assert resp.json() == dish_to_dict(test_dish)


async def test_dish_not_found(client, test_submenu):
    test_dish_id = uuid.uuid4()
    resp = await client.get(
        router_id.format(
            menu_id=test_submenu.menu_id,
            submenu_id=test_submenu.id, id=test_dish_id
        )
    )
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'dish not found'}


async def test_update_dish(client, async_session_test, test_submenu, test_dish):
     resp = await client.patch(
        router_id.format(
            menu_id=test_submenu.menu_id,
            submenu_id=test_submenu.id, id=test_dish.id
        ),
        json={
            'title': 'My updated dish',
            'description': 'My updated dish description',
            'price': '14.50',
        },
    )
     assert resp.status_code == 200
     updated_dish = await async_session_test.get(Dish, test_dish.id)
     assert resp.json() == dish_to_dict(updated_dish)


async def test_delete_dish(client, async_session_test, test_submenu, test_dish):
    resp = await client.delete(
        router_id.format(
            menu_id=test_submenu.menu_id,
            submenu_id=test_submenu.id, id=test_dish.id
        )
    )
    assert resp.status_code == 200
    deleted_dish = await async_session_test.get(Dish, test_dish.id)
    assert deleted_dish == None
    assert resp.json() == {
        'status': True,
        'message': 'The dish has been deleted',
    }



