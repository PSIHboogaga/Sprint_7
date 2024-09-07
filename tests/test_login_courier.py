import allure
import pytest
from data.test_data import TestCourier, CourierErrors
from data.courier_api import *
from data.urls import APIUrls

class TestAPICourierLogin:
    @allure.description('Проверка логина курьера | POST /api/v1/courier/login')
    @allure.title('Успешный вход курьера по логину и паролю')
    def test_courier_login_successful(self, test_user):
        login_courier = {"login": test_user[1][0],
                        "password": test_user[1][1]}
        r = requests.post(APIUrls.MAIN_URL + APIUrls.LOGIN_URL, data=login_courier)

        assert r.status_code == 200 and r.json()['id'] > 0

    @allure.description('Проверка логина с некорректными данными | POST /api/v1/courier/login')
    @allure.title('Получение ошибки при входе с некорректным паролем')
    def test_courier_login_wrong_password_failed(self, test_user):
        login_courier = {"login": test_user[1][1],
                        "password": test_user[1][0]}
        r = requests.post(APIUrls.MAIN_URL + APIUrls.LOGIN_URL, data=login_courier)

        assert r.status_code == 404 and r.json()['message'] == CourierErrors.login_no_such_user

    @allure.description('Проверка входа с не заполненными полями | POST /api/v1/courier/login')
    @allure.title('Получение ошибки с пустым полем логин')
    @pytest.mark.parametrize('user_data', (TestCourier.login_empty_login, TestCourier.login_empty_password, TestCourier.login_only_password))
    def test_courier_login_no_data_fail(self, user_data):
        r = requests.post(APIUrls.MAIN_URL + APIUrls.LOGIN_URL, data=user_data)

        assert r.status_code == 400 and r.json()['message'] == CourierErrors.login_no_data
