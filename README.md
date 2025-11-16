# How to execute tests

Please run on the main dir.

### Setup
```
pip install -r requirements.txt
export PREV_PYTHONPATH=$PYTHONPATH
export PYTHONPATH=$(pwd):$PYTHONPATH
```

### Test Run
```
pytest -rsx .
```

Result would be like
```
XFAIL test/test_menu_select.py::TestMenuSelect::test_menu_happy_case[valid_menu-quantity_0-shop_1-memberA]
XFAIL test/test_menu_select.py::TestMenuSelect::test_menu_happy_case[valid_menu-quantity_1-shop_1-memberA]
XFAIL test/test_menu_select.py::TestMenuSelect::test_menu_happy_case[valid_menu-quantity_99-shop_1-memberA]
XFAIL test/test_menu_select.py::TestMenuSelect::test_menu_invalid_menu[quantity_0-shop_1-memberA-invalid_menu]
XFAIL test/test_menu_select.py::TestMenuSelect::test_menu_invalid_menu[quantity_0-shop_1-memberA-empty_menu]
XFAIL test/test_menu_select.py::TestMenuSelect::test_menu_invalid_menu[quantity_1-shop_1-memberA-invalid_menu]
XFAIL test/test_menu_select.py::TestMenuSelect::test_menu_invalid_menu[quantity_1-shop_1-memberA-empty_menu]
XFAIL test/test_menu_select.py::TestMenuSelect::test_menu_invalid_menu[quantity_99-shop_1-memberA-invalid_menu]
XFAIL test/test_menu_select.py::TestMenuSelect::test_menu_invalid_menu[quantity_99-shop_1-memberA-empty_menu]
XFAIL test/test_menu_select.py::TestMenuSelect::test_menu_insufficient_ingredients[valid_menu-shop_1-memberA-quantity_negative]
XFAIL test/test_menu_select.py::TestMenuSelect::test_menu_insufficient_ingredients[valid_menu-shop_1-memberA-quantity_exceeds_ingredient]
XFAIL test/test_menu_select.py::TestMenuSelect::test_menu_insufficient_ingredients[valid_menu-shop_1-memberA-quantity_too_large]
XFAIL test/test_menu_select.py::TestMenuSelect::test_menu_invalid_shop[valid_menu-quantity_0-memberA-empty_shop]
XFAIL test/test_menu_select.py::TestMenuSelect::test_menu_invalid_shop[valid_menu-quantity_0-memberA-invalid_shop]
XFAIL test/test_menu_select.py::TestMenuSelect::test_menu_invalid_shop[valid_menu-quantity_1-memberA-empty_shop]
XFAIL test/test_menu_select.py::TestMenuSelect::test_menu_invalid_shop[valid_menu-quantity_1-memberA-invalid_shop]
XFAIL test/test_menu_select.py::TestMenuSelect::test_menu_invalid_shop[valid_menu-quantity_99-memberA-empty_shop]
XFAIL test/test_menu_select.py::TestMenuSelect::test_menu_invalid_shop[valid_menu-quantity_99-memberA-invalid_shop]
XFAIL test/test_order.py::TestOrder::test_order_succeed
XFAIL test/test_order.py::TestOrder::test_invalid_reservation_id
XFAIL test/test_order.py::TestOrder::test_reservation_id_expired
XFAIL test/test_order.py::TestOrder::test_invalid_member_no
XFAIL test/test_order.py::TestOrder::test_ingredients_exhausted
```
Please note that XFAILs are intended in the conftest.py

### Teardown
```
export PYTHONPATH=$PREV_PYTHONPATH
```


## Project Structures
* API/
    * menu_select.py - 메뉴 선택 API 처리
    * order.py - 주문 API 처리
    * api_client.py - API 호출을 위한 클라이언트 클래스 구현
    * types/ - API 요청 및 응답 데이터 모델 정의
* client.py - 기본 HTTP 요청 처리, 기본 헤더와 인증 토큰 설정
* test/ - pytest 기반의 테스트 정의

## 테스트 케이스 설명

### test_order.py
`test_order_succeed`
정상적인 주문

`test_invalid_reservation_id`
잘못된 예약 ID를 입력

`test_expired_reservation_id`
만료된 예약 ID를 입력

`test_invalid_member_no`
잘못된 회원 정보를 입력 - empty str, invalid ID

`test_invalid_ingredients_quantity`
선택된 메뉴의 개수가 유효하지 않은 경우

### test_menu_select.py
`test_menu_happy_case`
정상적인 메뉴 선택

`test_invalid_menu`
잘못된 메뉴 ID - empty str, invalid ID

`test_insufficient_ingredients`
선택된 메뉴의 개수가 유효하지 않은 경우 - quantity_negative, quantity_exceeds_ingredient, quantity_too_large, quantity_float

`test_menu_invalid_shop`
잘못된 가게 ID 입력 - empty str, invalid ID