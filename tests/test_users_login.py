import allure
import pytest
from helpers.api_data import ApiData


@allure.epic("Stellar Burgers API")
@allure.feature("Логин пользователя")
class TestLoginUser:
    
    @allure.title("Успешный вход под существующим пользователем")
    @allure.description("Тест проверяет успешную авторизацию с правильными учетными данными")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_login_existing_user_success(self, api_client, existing_user_credentials):
        with allure.step("Выполнить вход с корректными учетными данными"):
            response = api_client.login_user(
                email=existing_user_credentials["email"],
                password=existing_user_credentials["password"]
            )
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == ApiData.HTTP_OK, \
                f"Ожидался статус {ApiData.HTTP_OK}, получен {response.status_code}"
        
        with allure.step("Проверить структуру ответа"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_TRUE
            assert ApiData.KEY_ACCESS_TOKEN in response_data
            assert ApiData.KEY_REFRESH_TOKEN in response_data
            assert response_data[ApiData.KEY_USER][ApiData.KEY_EMAIL] == existing_user_credentials["email"]
            assert response_data[ApiData.KEY_USER][ApiData.KEY_NAME] == existing_user_credentials["name"]
        
        with allure.step("Проверить установку токена в клиенте"):
            assert api_client.token is not None

    @allure.title("Вход с неверным логином и паролем")
    @allure.description("Тест проверяет ошибку при входе с несуществующими учетными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_login_invalid_credentials_error(self, api_client, data_generator):
        with allure.step("Выполнить вход с неверными учетными данными"):
            user_data = data_generator.generate_user_data()
            response = api_client.login_user(
                email=user_data["email"],
                password=user_data["password"]
            )
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == ApiData.HTTP_UNAUTHORIZED, \
                f"Ожидался статус {ApiData.HTTP_UNAUTHORIZED}, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE
            assert ApiData.INVALID_CREDENTIALS_MESSAGE in response_data.get(ApiData.KEY_MESSAGE, "")
        
        with allure.step("Проверить отсутствие токена в клиенте"):
            assert api_client.token is None

    @allure.title("Вход с неверным паролем")
    @allure.description("Тест проверяет ошибку при входе с правильным email, но неправильным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_login_wrong_password_error(self, api_client, existing_user_credentials, data_generator):
        with allure.step("Выполнить вход с неправильным паролем"):
            wrong_password = data_generator.generate_password()
            response = api_client.login_user(
                email=existing_user_credentials["email"],
                password=wrong_password
            )
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == ApiData.HTTP_UNAUTHORIZED, \
                f"Ожидался статус {ApiData.HTTP_UNAUTHORIZED}, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE
            assert ApiData.INVALID_CREDENTIALS_MESSAGE in response_data.get(ApiData.KEY_MESSAGE, "")
        
        with allure.step("Проверить отсутствие токена в клиенте"):
            assert api_client.token is None

    @allure.title("Вход с неверным email")
    @allure.description("Тест проверяет ошибку при входе с правильным паролем, но неправильным email")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_login_wrong_email_error(self, api_client, existing_user_credentials, data_generator):
        with allure.step("Выполнить вход с неправильным email"):
            wrong_email = data_generator.generate_email()
            response = api_client.login_user(
                email=wrong_email,
                password=existing_user_credentials["password"]
            )
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == ApiData.HTTP_UNAUTHORIZED, \
                f"Ожидался статус {ApiData.HTTP_UNAUTHORIZED}, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE
            assert ApiData.INVALID_CREDENTIALS_MESSAGE in response_data.get(ApiData.KEY_MESSAGE, "")
        
        with allure.step("Проверить отсутствие токена в клиенте"):
            assert api_client.token is None

    @allure.title("Вход без email")
    @allure.description("Тест проверяет ошибку при входе без указания email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_login_without_email_error(self, api_client, existing_user_credentials):
        with allure.step("Выполнить вход без email"):
            response = api_client.login_user(
                email=None,
                password=existing_user_credentials["password"]
            )
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == ApiData.HTTP_UNAUTHORIZED, \
                f"Ожидался статус {ApiData.HTTP_UNAUTHORIZED}, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE

    @allure.title("Вход без пароля")
    @allure.description("Тест проверяет ошибку при входе без указания пароля")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_login_without_password_error(self, api_client, existing_user_credentials):
        with allure.step("Выполнить вход без пароля"):
            response = api_client.login_user(
                email=existing_user_credentials["email"],
                password=None
            )
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == ApiData.HTTP_UNAUTHORIZED, \
                f"Ожидался статус {ApiData.HTTP_UNAUTHORIZED}, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE