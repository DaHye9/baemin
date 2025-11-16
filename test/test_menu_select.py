import copy

import pytest

from api.api_client import APIClient
from api.types.menu_select import ErrorT, MenuSelectInfo, MenuSelectResponse


def pytest_generate_tests(metafunc: pytest.Metafunc):
    parametrize_markers = list(metafunc.definition.iter_markers('parametrize'))
    parametrized_fixtures: list = []
    if parametrize_markers:
        parametrized_fixtures = [marker.args[0] for marker in parametrize_markers]

    # Default parameterization
    # Happy path for menu selection
    # Unhappy path cases can be parametrized in individual tests
    if not parametrize_markers or 'menu_id' not in parametrized_fixtures:
        metafunc.parametrize('menu_id', ['menu'], ids=['valid_menu'])

    if not parametrize_markers or 'quantity' not in parametrized_fixtures:
        metafunc.parametrize(
            'quantity', [0, 1, 50], ids=['quantity_0', 'quantity_1', 'quantity_99']
        )

    if not parametrize_markers or 'shop_id' not in parametrized_fixtures:
        metafunc.parametrize('shop_id', ['shop_1'], ids=['shop_1'])

    if not parametrize_markers or 'member_no' not in parametrized_fixtures:
        metafunc.parametrize('member_no', ['memberA'], ids=['memberA'])


@pytest.fixture(scope='function', name='menu_info')
def fixture_menu_info(menu_id: str, quantity: int, shop_id: str, member_no: str) -> MenuSelectInfo:
    return MenuSelectInfo(menuId=menu_id, quantity=quantity, shopId=shop_id, memberNo=member_no)


def validate_menu_select_succeed(
    response: MenuSelectResponse, expected_menu_id: str, expected_quantity: int
) -> None:
    assert response.status == 'SUCCESS'
    assert response.data
    assert response.data.menuId == expected_menu_id
    assert response.data.quantity == expected_quantity


def validate_menu_select_failed(
    response: MenuSelectResponse,
    expected_error_code: ErrorT,
) -> None:
    # NOTE: message is not validated here since it may vary.
    assert response.status == 'ERROR'
    assert response.error_code == expected_error_code
    assert not response.data


class TestMenuSelect:
    def test_menu_happy_case(self, client: APIClient, menu_info: MenuSelectInfo):
        """Post a valid menu selection and expect success and correct data."""
        response = client.menu_select.post(menu_info)
        validate_menu_select_succeed(
            response, expected_menu_id=menu_info.menuId, expected_quantity=menu_info.quantity
        )

    @pytest.mark.parametrize('menu_id', ['invalid_menu', ''], ids=['invalid_menu', 'empty_menu'])
    def test_invalid_menu(self, client: APIClient, menu_info: MenuSelectInfo, menu_id: str):
        """Post a menu selection with an invalid menu ID and expect an error."""
        menu_info.menuId = menu_id
        response = client.menu_select.post(menu_info)
        validate_menu_select_failed(response, expected_error_code='MENU_NOT_FOUND')

    @pytest.mark.parametrize(
        'quantity',
        [-1, 99, 1000, 1.5],
        ids=[
            'quantity_negative',
            'quantity_exceeds_ingredient',
            'quantity_too_large',
            'quantity_float',
        ],
    )
    def test_insufficient_ingredients(
        self, client: APIClient, menu_info: MenuSelectInfo, quantity: float
    ):
        """Post a menu selection with an invalid quantity and expect an error."""
        menu_info = copy.deepcopy(menu_info)
        menu_info.quantity = quantity
        response = client.menu_select.post(menu_info)
        validate_menu_select_failed(response, expected_error_code='INSUFFICIENT_INGREDIENTS')

    @pytest.mark.parametrize('shop_id', ['', 'invalid_shop'], ids=['empty_shop', 'invalid_shop'])
    def test_menu_invalid_shop(self, client: APIClient, menu_info: MenuSelectInfo, shop_id: str):
        """Post a menu selection with an invalid shop ID and expect an error."""
        menu_info = copy.deepcopy(menu_info)
        menu_info.shopId = shop_id
        response = client.menu_select.post(menu_info)
        validate_menu_select_failed(response, expected_error_code='INVALID REQUEST')
