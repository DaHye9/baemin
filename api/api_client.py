from api import menu_select, order
from client import Client


class APIClient(Client):
    """API Client for Food Delivery Service extending the base Client."""

    def __init__(self) -> None:
        super().__init__()

    @property
    def menu_select(self) -> menu_select.MenuSelect:
        return menu_select.MenuSelect(self)

    @property
    def order(self) -> order.Order:
        return order.Order(self)
