import sender_stand_request
import data


def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


def positive_assert(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(user_body)


def test_create_user_2_letter_in_first_name_get_success_response():
    user_body = get_user_body("Аа")
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1


def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Ааааааааааааааа")


def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()[
               "message"] == "Имя пользователя введено некорректно. Имя может содержать только русские или латинские буквы, длина должна быть не менее 2 и не более 15 символов"


def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")


def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("Аааааааааааааааа")

def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("QWErty")

def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Мария")

def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("Человек и Ко")

def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("№%@")

def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("123")

def negative_assert_no_first_name(user_body):
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Unexpected token \" in JSON at position 0"

def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_no_first_name()

# Тест 11. Ошибка
# Параметр fisrtName состоит из пустой строки
def test_create_user_empty_first_name_get_error_response():
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body("")
    # Проверка полученного ответа
    negative_assert_no_first_name(user_body)

def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400