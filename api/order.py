from api.types.order import OrderRequest, OrderResponse
from client import Client


class Order:
    def __init__(self, client: Client) -> None:
        self._client = client

    def post(self, order: OrderRequest) -> OrderResponse:
        """Create an order."""
        route = '/api/v1/order/create'
        res = self._client.post(
            route, 
            {
                'reservationId': order.reservationId,
                'memberNo': order.memberNo
            }
        )
        return OrderResponse(res.json())
