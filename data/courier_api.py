import requests
import random
import string
import json
from data.test_data import TestOrder
from data.urls import APIUrls
import allure

@allure.step("Регистация нового курьера и возвращение логина, пароля")
def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(APIUrls.MAIN_URL + APIUrls.COURIER_URL, data=payload)
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return response, login_pass

@allure.step("Получение несуществующего ID курьера")
def non_existing_id_courier():
    courier = register_new_courier_and_return_login_password()
    sign_in = {
        "login": courier[1][0],
        "password": courier[1][1]
    }

    courier_signin = requests.post(APIUrls.MAIN_URL + APIUrls.LOGIN_URL, data=sign_in)
    courier_id = courier_signin.json()["id"] + random.randint(1000, 9000)
    return courier_id

@allure.step("Вернуть новый заказ")
def return_new_order():
    payload = json.dumps(TestOrder.test_order)
    response = requests.post(APIUrls.MAIN_URL + APIUrls.MAIN_ORDERS_URL, data=payload)
    track = response.json()["track"]
    return track