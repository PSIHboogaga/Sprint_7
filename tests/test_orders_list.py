import allure
from data.courier_api import *
from data.urls import APIUrls

class TestGetOrdersList:

    @allure.description("Получение списка заказов | GET /api/v1/orders")
    @allure.title('Успешное получение списка заказов')
    def test_get_orders_list_success(self):
        response = requests.get(APIUrls.MAIN_URL + APIUrls.MAIN_ORDERS_URL)
        orders_list = response.json()["orders"]
        assert response.status_code == 200 and isinstance(orders_list, list) == True