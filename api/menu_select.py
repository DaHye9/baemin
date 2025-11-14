from api.types.menu_select import MenuSelectInfo, MenuSelectResponse
from client import Client


class MenuSelect:
    def __init__(self, client: Client) -> None:
        self._client = client

    def post(self, menu_info: MenuSelectInfo) -> MenuSelectResponse:
        """Post a menu selection from user."""
        route = '/api/v1/menu/select'
        res = self._client.post(
            route,
            {
                'menuId': menu_info.menuId,
                'quantity': menu_info.quantity,
                'shopId': menu_info.shopId,
                'memberNo': menu_info.memberNo
            }
        )
        return MenuSelectResponse(res.json())
