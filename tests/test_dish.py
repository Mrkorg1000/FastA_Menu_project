from conftest import *
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



def test_get_empty_dish_list(client, test_menu, test_submenu):
    resp = client.get(router.format(menu_id=test_menu.id, submenu_id=test_submenu.id))
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_dish(client, session_test, test_menu, test_submenu):
    resp = client.post(
        router.format(menu_id=test_menu.id, submenu_id=test_submenu.id),
        json={'title': 'My super dish', 'description': 'My super dish description',
              'price': '12.50',
        },
    )
    assert resp.status_code == 201
    dish_id = resp.json()["id"]
    dish = session_test.query(Dish).\
        filter(Dish.id==dish_id).first()
    assert resp.json() == dish_to_dict(dish)


def test_get_dish_list(client, session_test):
    submenu = session_test.query(Submenu).one()
    menu = session_test.query(Menu).one()
    resp = client.get(router.format(
        menu_id=menu.id, submenu_id=submenu.id)
    )
    assert resp.status_code == 200
    dish_list = session_test.query(Dish).all()
    assert resp.json() == [dish_to_dict(dish)
                           for dish in dish_list]


def test_get_dish_by_id(client, session_test):
    dish = session_test.query(Dish).one()
    submenu = session_test.query(Submenu).one()
    menu = session_test.query(Menu).one()

    resp = client.get(
        router_id.format(menu_id=menu.id, submenu_id=submenu.id,
        id=dish.id)
    )
    assert resp.status_code == 200
    assert resp.json() == dish_to_dict(dish)


def test_dish_not_found(client, session_test):
    submenu = session_test.query(Submenu).one()
    menu = session_test.query(Menu).one()
    test_dish_id = uuid.uuid4()
    resp = client.get(
        router_id.format(
            menu_id=menu.id,
            submenu_id=submenu.id, id=test_dish_id
        )
    )
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'dish not found'}


def test_update_dish(client, session_test):
    submenu = session_test.query(Submenu).one()
    menu = session_test.query(Menu).one()
    dish = session_test.query(Dish).one()
    resp = client.patch(
        router_id.format(
            menu_id=menu.id,
            submenu_id=submenu.id, id=dish.id
        ),
        json={
            'title': 'My updated dish',
            'description': 'My updated dish description',
            'price': '14.50',
        },
    )
    assert resp.status_code == 200
    updated_dish = session_test.query(Dish).\
        filter(Dish.id == dish.id).first()
    assert resp.json() == dish_to_dict(updated_dish)


def test_delete_dish(client, session_test):
    submenu = session_test.query(Submenu).one()
    menu = session_test.query(Menu).one()
    dish = session_test.query(Dish).one()
    resp = client.delete(
        router_id.format(
            menu_id=menu.id,
            submenu_id=submenu.id, id=dish.id
        )
    )
    assert resp.status_code == 200
    deleted_dish = session_test.query(Dish).\
        filter(Dish.id == dish.id).first()
    assert deleted_dish == None
    assert resp.json() == {
        'status': True,
        'message': 'The dish has been deleted',
    }



