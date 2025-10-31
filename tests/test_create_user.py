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
        token = None
        try:
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
                    f"Ожидался статус {ApiData.HTTP_OK}, получен {response.status_code}. Response: {response.text}"
            
            with allure.step("Проверить структуру ответа"):
                response_data = response.json()
                assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_TRUE
                assert ApiData.KEY_ACCESS_TOKEN in response_data
                assert ApiData.KEY_REFRESH_TOKEN in response_data
                assert response_data[ApiData.KEY_USER][ApiData.KEY_EMAIL] == user_data["email"]
                assert response_data[ApiData.KEY_USER][ApiData.KEY_NAME] == user_data["name"]
                
                token = response_data[ApiData.KEY_ACCESS_TOKEN]
                
        finally:
            if token:
                with allure.step("Удалить созданного пользователя"):
                    api_client.delete_user(token)

    @allure.title("Создание пользователя с существующим email - ошибка 403")
    @allure.description("Тест проверяет ошибку 403 при попытке создания пользователя с существующим email")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_create_duplicate_user_forbidden_error(self, api_client, registered_user_success):
        with allure.step("Попытаться создать пользователя с существующим email"):
            response = api_client.register_user(
                email=registered_user_success["email"],
                password=registered_user_success["password"],
                name=registered_user_success["name"]
            )
        
        with allure.step("Проверить статус код ответа 403"):
            assert response.status_code == ApiData.HTTP_FORBIDDEN, \
                f"Ожидался статус {ApiData.HTTP_FORBIDDEN}, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE
            assert ApiData.USER_EXISTS_MESSAGE in response_data.get(ApiData.KEY_MESSAGE, "")

    @allure.title("Создание пользователя с существующим email - ошибка 400")
    @allure.description("Тест проверяет ошибку 400 при попытке создания пользователя с существующим email")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    @pytest.mark.mock_api
    def test_create_duplicate_user_bad_request_error(self, api_client, registered_user_success):
        """Этот тест может работать только с мок-API, так как реальное API возвращает 403"""
        with allure.step("Попытаться создать пользователя с существующим email"):
            response = api_client.register_user(
                email=registered_user_success["email"],
                password=registered_user_success["password"],
                name=registered_user_success["name"]
            )
        
        with allure.step("Проверить статус код ответа 400"):
            assert response.status_code == ApiData.HTTP_BAD_REQUEST, \
                f"Ожидался статус {ApiData.HTTP_BAD_REQUEST}, получен {response.status_code}"
        
        with allure.step("Проверить наличие ошибки в ответе"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE

    @allure.title("Создание пользователя без email")
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
            assert response.status_code == ApiData.HTTP_BAD_REQUEST, \
                f"Ожидался статус {ApiData.HTTP_BAD_REQUEST}, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE
            assert ApiData.REQUIRED_FIELDS_MESSAGE in response_data.get(ApiData.KEY_MESSAGE, "")

    @allure.title("Создание пользователя без пароля")
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
            assert response.status_code == ApiData.HTTP_BAD_REQUEST, \
                f"Ожидался статус {ApiData.HTTP_BAD_REQUEST}, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE
            assert ApiData.REQUIRED_FIELDS_MESSAGE in response_data.get(ApiData.KEY_MESSAGE, "")

    @allure.title("Создание пользователя без имени")
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
            assert response.status_code == ApiData.HTTP_BAD_REQUEST, \
                f"Ожидался статус {ApiData.HTTP_BAD_REQUEST}, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE
            assert ApiData.REQUIRED_FIELDS_MESSAGE in response_data.get(ApiData.KEY_MESSAGE, "")

            