from api.types.order import OrderRequest, PostResponse
from client import Client


class Order:
    def __init__(self, client: Client) -> None:
        self._client = client

    def post(self, order: OrderRequest) -> PostResponse:
        """Create an order."""
        route = '/api/v1/order/create'
        res = self._client.post(
            route, 
            {
                'reservationId': order.reservationId,
                'memberNo': order.memberNo
            }
        )
        return PostResponse(res.json())
