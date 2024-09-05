import datetime
from datetime import date as d


class TestCourier:
    login_only_password = {"password": "qwerty"}
    login_empty_password = {"login": "tester", "password": ""}
    login_empty_login = {"login": "", "password": "qwerty!"}

    create_no_login_courier = {"password": "qwerty", "firstName": "Andrey"}
    create_no_password_courier = {"login": "tester", "firstName": "Andrey"}
    create_empty_login = {"login": "", "password": "qwerty", "firstName": "Andrey"}
    create_empty_password = {"login": "tester", "password": "", "firstName": "Andrey"}


class TestOrder:
    delivery_date = (d.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    test_order = {"order":
{
    "firstName": "Ivan",
    "lastName": "Ivanov",
    "address": "Lenina, 8 ",
    "metroStation": 4,
    "phone": "+7 999 888 88 88",
    "rentTime": 5,
    "deliveryDate": "2024-05-24",
    "comment": "проверка комментария",
    "color": ["BLACK"]
 }
    }


class OrdersErrors:
    track_order_no_data = "Недостаточно данных для поиска"
    track_order_no_such_order = "Заказ не найден"

    accept_order_no_order_number = "Недостаточно данных для поиска"
    accept_order_no_such_courier = "Курьера с таким id не существует"
    accept_order_no_data = "Недостаточно данных для поиска"


class CourierErrors:
    create_no_data = "Недостаточно данных для создания учетной записи"
    create_already_exist = "Этот логин уже используется. Попробуйте другой."

    login_no_data = "Недостаточно данных для входа"
    login_no_such_user = "Учетная запись не найдена"