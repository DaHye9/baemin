from datetime import datetime

import pytest

from api.api_client import APIClient
from api.types.menu_select import MenuSelectInfo
from api.types.order import ErrorT, OrderRequest, OrderResponse


@pytest.fixture(scope='function', name='valid_reservation_id')
def fixture_valid_reservation_id(client: APIClient, valid_member_no: str) -> str:
    # Valid menu selection to create a reservation
    menu_select_res = client.menu_select.post(
        MenuSelectInfo(menuId='menu', quantity=1, shopId='shop_1', memberNo=valid_member_no)
    )
    return menu_select_res.data.reservationId


@pytest.fixture(scope='function', name='valid_member_no')
def fixture_valid_member_no() -> str:
    return 'memberA'


@pytest.fixture(scope='function', name='invalid_reservation_id_time_expired')
def fixture_invalid_reservation_id_time_expired() -> str:
    # Simulate an expired reservation ID
    # This could include expiration time in database
    # Or, just wait for the reservation to expire in a real test
    return 'expired_reservation_123'


def validate_order_succeed(
    response: OrderResponse,
    expected_reservation_id: str,
    expected_member_no: str,
    after_time: datetime,
) -> None:
    assert response.status == 'SUCCESS'
    assert response.data
    assert response.data.orderStatus == 'INITIALIZING'
    assert datetime.utcnow() >= response.data.createdAt >= after_time
    assert response.data.reservationId == expected_reservation_id
    assert response.data.memberInfo.memberNo == expected_member_no


def validate_order_failed(
    response: OrderResponse,
    expected_error_code: ErrorT,
) -> None:
    # NOTE: message is not validated here since it may vary.
    assert response.status == 'ERROR'
    assert response.error_code == expected_error_code
    assert not response.data


class TestOrder:
    def test_order_succeed(
        self, client: APIClient, valid_reservation_id: str, valid_member_no: str
    ) -> None:
        after_time = datetime.utcnow()
        order_req = OrderRequest(
            reservationId=valid_reservation_id,
            memberNo=valid_member_no,
        )
        response = client.order.post(order_req)
        validate_order_succeed(response, valid_reservation_id, valid_member_no, after_time)

    @pytest.mark.parametrize(
        'reservation_id',
        ['', 'invalid_reservation_123'],
        ids=['empty_reservation_id', 'invalid_reservation_id'],
    )
    def test_invalid_reservation_id(
        self,
        client: APIClient,
        valid_member_no: str,
        reservation_id: str,
    ) -> None:
        """Test ordering with an invalid reservation ID."""
        order_req = OrderRequest(reservationId=reservation_id, memberNo=valid_member_no)
        response = client.order.post(order_req)
        validate_order_failed(response, expected_error_code='INVALID_RESERVATION')

    def test_expired_reservation_id(
        self,
        client: APIClient,
        invalid_reservation_id_time_expired: str,
        valid_member_no: str,
    ) -> None:
        order_req = OrderRequest(
            reservationId=invalid_reservation_id_time_expired,
            memberNo=valid_member_no,
        )
        response = client.order.post(order_req)
        validate_order_failed(response, expected_error_code='RESERVATION_EXPIRED')

    @pytest.mark.parametrize(
        'invalid_member_no',
        ['', 'invalid_member_123'],
        ids=['empty_member_no', 'invalid_member_no'],
    )
    def test_invalid_member_no(
        self,
        client: APIClient,
        valid_reservation_id: str,
        invalid_member_no: str,
    ) -> None:
        """Test ordering with an reservation ID that does not match the member no."""
        order_req = OrderRequest(
            reservationId=valid_reservation_id,
            memberNo=invalid_member_no,
        )
        response = client.order.post(order_req)
        validate_order_failed(response, expected_error_code='INVALID_RESERVATION')

    @pytest.mark.parametrize(
        'quantity', [0, 1000], ids=['quantity_zero', 'quantity_exceeds_ingredient']
    )
    def test_invalid_ingredients_quantity(
        self,
        client: APIClient,
        valid_member_no: str,
        quantity: int,
    ) -> None:
        """Test ordering when ingredients are exhausted."""
        menu_select_res = client.menu_select.post(
            MenuSelectInfo(
                menuId='menu', quantity=quantity, shopId='shop_1', memberNo=valid_member_no
            )
        )
        reservation_id = menu_select_res.data.reservationId

        order_req = OrderRequest(
            reservationId=reservation_id,
            memberNo=valid_member_no,
        )
        response = client.order.post(order_req)
        validate_order_failed(response, expected_error_code='INGREDIENTS_EXHAUSTED')
