import allure
import pytest
from helpers.api_data import ApiData


@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestCreateUser:
    
    @allure.title("Создание уникального пользователя")
    @allure.description("Тест проверяет успешное создание нового пользователя с валидными данными")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_create_unique_user_success(self, api_client, data_generator):
        with allure.step("Подготовить данные для нового пользователя"):
            user_data = data_generator.generate_user_data()
        
        with allure.step("Отправить запрос на создание пользователя"):
            response = api_client.register_user(
                email=user_data["email"],
                password=user_data["password"],
                name=user_data["name"]
            )
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == ApiData.HTTP_OK, \
                f"Ожидался статус {ApiData.HTTP_OK}, получен {response.status_code}"
        
        with allure.step("Проверить структуру ответа"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_TRUE
            assert ApiData.KEY_ACCESS_TOKEN in response_data
            assert ApiData.KEY_REFRESH_TOKEN in response_data
            assert response_data[ApiData.KEY_USER][ApiData.KEY_EMAIL] == user_data["email"]
            assert response_data[ApiData.KEY_USER][ApiData.KEY_NAME] == user_data["name"]
        
        with allure.step("Удалить созданного пользователя"):
            api_client.delete_user(response_data[ApiData.KEY_ACCESS_TOKEN])

    @allure.title("Создание пользователя, который уже зарегистрирован")
    @allure.description("Тест проверяет ошибку при попытке создания пользователя с существующим email")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_create_duplicate_user_error(self, api_client, existing_user_credentials):
        with allure.step("Попытаться создать пользователя с существующим email"):
            response = api_client.register_user(
                email=existing_user_credentials["email"],
                password=existing_user_credentials["password"],
                name=existing_user_credentials["name"]
            )
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == ApiData.HTTP_FORBIDDEN, \
                f"Ожидался статус {ApiData.HTTP_FORBIDDEN}, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE
            assert ApiData.USER_EXISTS_MESSAGE in response_data.get(ApiData.KEY_MESSAGE, "")

    @allure.title("Создание пользователя без обязательного поля email")
    @allure.description("Тест проверяет ошибку при создании пользователя без email")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_create_user_without_email_error(self, api_client, data_generator):
        with allure.step("Создать пользователя без email"):
            user_data = data_generator.generate_user_without_email()
            response = api_client.register_user(
                email=user_data["email"],
                password=user_data["password"],
                name=user_data["name"]
            )
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == ApiData.HTTP_FORBIDDEN, \
                f"Ожидался статус {ApiData.HTTP_FORBIDDEN}, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE
            assert ApiData.REQUIRED_FIELDS_MESSAGE in response_data.get(ApiData.KEY_MESSAGE, "")

    @allure.title("Создание пользователя без обязательного поля password")
    @allure.description("Тест проверяет ошибку при создании пользователя без пароля")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_create_user_without_password_error(self, api_client, data_generator):
        with allure.step("Создать пользователя без пароля"):
            user_data = data_generator.generate_user_without_password()
            response = api_client.register_user(
                email=user_data["email"],
                password=user_data["password"],
                name=user_data["name"]
            )
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == ApiData.HTTP_FORBIDDEN, \
                f"Ожидался статус {ApiData.HTTP_FORBIDDEN}, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE
            assert ApiData.REQUIRED_FIELDS_MESSAGE in response_data.get(ApiData.KEY_MESSAGE, "")

    @allure.title("Создание пользователя без обязательного поля name")
    @allure.description("Тест проверяет ошибку при создании пользователя без имени")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_create_user_without_name_error(self, api_client, data_generator):
        with allure.step("Создать пользователя без имени"):
            user_data = data_generator.generate_user_without_name()
            response = api_client.register_user(
                email=user_data["email"],
                password=user_data["password"],
                name=user_data["name"]
            )
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == ApiData.HTTP_FORBIDDEN, \
                f"Ожидался статус {ApiData.HTTP_FORBIDDEN}, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE
            assert ApiData.REQUIRED_FIELDS_MESSAGE in response_data.get(ApiData.KEY_MESSAGE, "")