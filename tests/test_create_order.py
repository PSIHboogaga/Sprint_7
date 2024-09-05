import allure
import pytest
from data.courier_api import *
from data.test_data import OrdersErrors
from data.urls import APIUrls


class TestCreateOrder:

    @allure.description('Проверка создания заказа с несколькими вариантами цветов | POST /api/v1/orders')
    @allure.title('Успешное создание заказа с несколькими цветами')
    @pytest.mark.parametrize('color', (["BLACK"], ["GREY"], ["BLACK", "GREY"], []))
    def test_create_order_with_different_colors_successful(self, color):
        TestOrder.test_order["color"] = [color]
        payload = json.dumps(TestOrder.test_order)
        response = requests.post(APIUrls.MAIN_URL + APIUrls.MAIN_ORDERS_URL, data=payload)
        assert response.status_code == 201 and 'track' in response.text


class TestTrackingOrder:
    @allure.description('Проверка получения данных о заказе | GET /api/v1/orders/track')
    @allure.title('Успешное получение данных о заказе')
    def test_order_tracking_successful(self):
        new_track = return_new_order()
        payload = {"t": new_track}
        response = requests.get(APIUrls.MAIN_URL + APIUrls.TRACK_ORDER_URL + str(new_track), data=payload)
        assert response.status_code == 200 and 'order' in response.text

    @allure.description('Проверка получения данных о заказе без номера | GET /api/v1/orders/track')
    @allure.title('Получение ошибки данных о заказе без номера')
    def test_order_track_no_order_id_failed(self):
        new_track = return_new_order()
        payload = {"t": new_track}
        response = requests.get(APIUrls.MAIN_URL + APIUrls.TRACK_ORDER_URL, data=payload)

        assert response.status_code == 400 and response.json()['message'] == OrdersErrors.track_order_no_data

    @allure.description('Проверка получения данных о заказе с несуществующим номером | GET /api/v1/orders/track')
    @allure.title('Получение ошибки данных о несуществующем заказе')
    def test_order_track_bad_order_failed(self):
        new_track = 0
        payload = {"t": new_track}
        response = requests.get(APIUrls.MAIN_URL + APIUrls.TRACK_ORDER_URL + str(new_track), data=payload)
        assert response.status_code == 404 and response.json()['message'] == OrdersErrors.track_order_no_such_order


class TestGetOrder:

    @allure.description('Проверка принятия заказа курьером | POST /api/v1/courier/login')
    @allure.title('Успешное принятие заказа курьером')
    def test_courier_get_order_successful(self, test_signin_user_id):
        new_track = return_new_order()
        track_order = requests.get(APIUrls.MAIN_URL + APIUrls.TRACK_ORDER_URL + str(new_track))
        order_id = track_order.json()['order']['id']

        payload = {"id": order_id,
                   "courierId": test_signin_user_id}
        response = requests.put(
            APIUrls.MAIN_URL + APIUrls.ACCEPT_ORDER_URL + str(order_id) + '?courierId=' + str(
                test_signin_user_id), data=payload)

        assert response.status_code == 200 and response.json()['ok'] == True

    @allure.description('Проверка принятия заказа с неверным id курьера | GET /api/v1/orders/track')
    @allure.title('Получение ошибки приема заказа с некорректным id курьера')
    def test_get_order_with_bad_courier_id_fail(self):
        courier_id = non_existing_id_courier()
        new_track = return_new_order()
        track_order = requests.get(APIUrls.MAIN_URL + APIUrls.TRACK_ORDER_URL + str(new_track))
        order_id = track_order.json()['order']['id']

        payload = {"id": order_id,
                   "courierId": courier_id}
        response = requests.put(
            APIUrls.MAIN_URL + APIUrls.ACCEPT_ORDER_URL + str(order_id) + '?courierId=' + str(
                courier_id), data=payload)

        assert response.status_code == 404 and response.json()['message'] == OrdersErrors.accept_order_no_such_courier
