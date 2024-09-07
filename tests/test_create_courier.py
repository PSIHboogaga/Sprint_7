import pytest
from data.courier_api import *
from data.test_data import TestCourier, CourierErrors
from data.urls import APIUrls


class TestAPICourierCreate:
    @allure.description('Проверка успешного создания курьера | POST /api/v1/courier')
    @allure.title('Курьер создается')
    def test_create_new_courier_successful(self, create_and_delete_courier):
        courier_signin = requests.post(APIUrls.MAIN_URL + APIUrls.COURIER_URL, data=create_and_delete_courier)

        assert courier_signin.status_code == 201 and courier_signin.json()['ok'] is True

    @allure.description('Проверка на создание дубликата курьера | POST /api/v1/courier')
    @allure.title('Получение ошибки при создании дубликата курьера')
    def test_create_double_courier_is_failed(self, create_and_delete_courier):
        requests.post(APIUrls.MAIN_URL + APIUrls.COURIER_URL, data=create_and_delete_courier)
        courier_signin_2 = requests.post(APIUrls.MAIN_URL + APIUrls.COURIER_URL, data=create_and_delete_courier)
        assert courier_signin_2.status_code == 409 and courier_signin_2.json()['message'] == CourierErrors.create_already_exist

    @allure.description('Проверка создания курьера без обязательных полей | POST /api/v1/courier')
    @allure.title('Получение ошибки при создание курьера без обязательных полей')
    @pytest.mark.parametrize('user_data', (TestCourier.create_no_login_courier, TestCourier.create_no_password_courier,
                                  TestCourier.create_empty_login, TestCourier.create_empty_password))
    def test_create_courier_without_data_failed(self, user_data):
        r = requests.post(APIUrls.MAIN_URL + APIUrls.COURIER_URL, data=user_data)

        assert r.status_code == 400 and r.json()['message'] == CourierErrors.create_no_data
