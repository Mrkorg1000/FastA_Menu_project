from conftest import *
from database.models import Dish
import uuid

router = '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes'
router_id = 'api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{id}'

# Тестовый сценарий: Исходное состояние -> БД пустая.
# 1. Вывод пустого списка блюд. 2. Создание блюда.
# 3. Вывод списка блюд. 4. Получение блюда по id.
# 5. Получение блюда по несуществующему id.
# 6. Изменеие блюда
# 7. Удаление блюда.



def test_get_empty_dish_list(client, create_menu_submenu_ids):
    menu_id, submenu_id = create_menu_submenu_ids
    resp = client.get(router.format(menu_id=menu_id, submenu_id=submenu_id))
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_dish(client, session_test, menu_id_from_db, submenu_id_from_db):
    resp = client.post(
        router.format(menu_id=menu_id_from_db, submenu_id=submenu_id_from_db),
        json={'title': 'My super dish', 'description': 'My super dish description',
              'price': '12.50',
        },
    )
    assert resp.status_code == 201
    id = resp.json()["id"]
    dish = get_dish_by_id(session_test, id)
    assert resp.json() == dish_to_dict(dish)


def test_get_dish_list(client, session_test, menu_id_from_db, submenu_id_from_db):
    resp = client.get(router.format(
        menu_id=menu_id_from_db, submenu_id=submenu_id_from_db)
    )
    assert resp.status_code == 200
    dish_list = session_test.query(Dish).all()
    assert resp.json() == [dish_to_dict(dish)
                           for dish in dish_list]


def test_get_dish_by_id(client, session_test, menu_id_from_db, submenu_id_from_db):
    dish = session_test.query(Dish).one()
    dish_id = dish.id
    resp = client.get(
        router_id.format(menu_id=menu_id_from_db, submenu_id=submenu_id_from_db,
        id=dish_id)
    )
    assert resp.status_code == 200
    assert resp.json() == dish_to_dict(dish)


def test_dish_not_found(client, session_test, menu_id_from_db, submenu_id_from_db):
    test_id = uuid.uuid4()
    resp = client.get(
        router_id.format(
            menu_id=menu_id_from_db,
            submenu_id=submenu_id_from_db, id=test_id
        )
    )
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'dish not found'}


def test_update_dish(client, session_test, menu_id_from_db, submenu_id_from_db):
    dish = session_test.query(Dish).one()
    dish_id = dish.id
    resp = client.patch(
        router_id.format(
            menu_id=menu_id_from_db,
            submenu_id=submenu_id_from_db, id=dish_id
        ),
        json={
            'title': 'My updated dish',
            'description': 'My updated dish description',
            'price': '14.50',
        },
    )
    assert resp.status_code == 200
    assert resp.json() == dish_to_dict(dish)


def test_delete_dish(client, session_test, menu_id_from_db, submenu_id_from_db):
    dish = session_test.query(Dish).one()
    dish_id = dish.id
    resp = client.delete(
        router_id.format(
            menu_id=menu_id_from_db,
            submenu_id=submenu_id_from_db, id=dish_id
        )
    )
    assert resp.status_code == 200
    assert resp.json() == {
        'status': True,
        'message': 'The dish has been deleted',
    }



