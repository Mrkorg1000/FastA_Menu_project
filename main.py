import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from api.endpoints import menu, submenu, dish

# application instance
app = FastAPI(title="menu_project")

# main api router instance
main_api_router = APIRouter()

main_api_router.include_router(
    menu.router,
    prefix="/api/v1/menus",
    tags=["menus"]
)

main_api_router.include_router(
    submenu.router,
    prefix="/api/v1/menus/{menu_id}/submenus",
    tags=["submenus"]
)


main_api_router.include_router(
    dish.router,
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["dishes"]
)


app.include_router(main_api_router)

