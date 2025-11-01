import allure
import pytest
from helpers.api_data import ApiData


@allure.epic("Stellar Burgers API")
@allure.feature("Логин пользователя")
class TestLoginUser:
    
    @allure.title("Успешный вход под существующим пользователем - успех 200")
    @allure.description("Тест проверяет успешную авторизацию с правильными учетными данными")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_login_existing_user_success_200(self, api_client, existing_user_credentials):
        with allure.step("Выполнить вход с корректными учетными данными"):
            response = api_client.login_user(
                email=existing_user_credentials["email"],
                password=existing_user_credentials["password"]
            )
        
        with allure.step("Проверить статус код ответа 200"):
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

    @allure.title("Вход с неверным логином и паролем - ошибка 401")
    @allure.description("Тест проверяет ошибку при входе с несуществующими учетными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_login_invalid_credentials_error_401(self, api_client, data_generator):
        with allure.step("Выполнить вход с неверными учетными данными"):
            user_data = data_generator.generate_user_data()
            response = api_client.login_user(
                email=user_data["email"],
                password=user_data["password"]
            )
        
        with allure.step("Проверить статус код ответа 401"):
            assert response.status_code == ApiData.HTTP_UNAUTHORIZED, \
                f"Ожидался статус {ApiData.HTTP_UNAUTHORIZED}, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE
            assert ApiData.INVALID_CREDENTIALS_MESSAGE in response_data.get(ApiData.KEY_MESSAGE, "")
        
        with allure.step("Проверить отсутствие токена в клиенте"):
            assert api_client.token is None

    @allure.title("Вход с неверным паролем - ошибка 401")
    @allure.description("Тест проверяет ошибку при входе с правильным email, но неправильным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_login_wrong_password_error_401(self, api_client, existing_user_credentials, data_generator):
        with allure.step("Выполнить вход с неправильным паролем"):
            wrong_password = data_generator.generate_password()
            response = api_client.login_user(
                email=existing_user_credentials["email"],
                password=wrong_password
            )
        
        with allure.step("Проверить статус код ответа 401"):
            assert response.status_code == ApiData.HTTP_UNAUTHORIZED, \
                f"Ожидался статус {ApiData.HTTP_UNAUTHORIZED}, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE
            assert ApiData.INVALID_CREDENTIALS_MESSAGE in response_data.get(ApiData.KEY_MESSAGE, "")
        
        with allure.step("Проверить отсутствие токена в клиенте"):
            assert api_client.token is None

    @allure.title("Вход с неверным email - ошибка 401")
    @allure.description("Тест проверяет ошибку при входе с правильным паролем, но неправильным email")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_login_wrong_email_error_401(self, api_client, existing_user_credentials, data_generator):
        with allure.step("Выполнить вход с неправильным email"):
            wrong_email = data_generator.generate_email()
            response = api_client.login_user(
                email=wrong_email,
                password=existing_user_credentials["password"]
            )
        
        with allure.step("Проверить статус код ответа 401"):
            assert response.status_code == ApiData.HTTP_UNAUTHORIZED, \
                f"Ожидался статус {ApiData.HTTP_UNAUTHORIZED}, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE
            assert ApiData.INVALID_CREDENTIALS_MESSAGE in response_data.get(ApiData.KEY_MESSAGE, "")
        
        with allure.step("Проверить отсутствие токена в клиенте"):
            assert api_client.token is None

    @allure.title("Успешный вход после регистрации - успех 200")
    @allure.description("Тест проверяет успешную авторизацию сразу после регистрации пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    def test_login_after_registration_success_200(self, api_client, registered_user_success):
        with allure.step("Выполнить вход с только что созданными учетными данными"):
            login_response = api_client.login_user(
                email=registered_user_success["email"],
                password=registered_user_success["password"]
            )
        
        with allure.step("Проверить статус код ответа 200"):
            assert login_response.status_code == ApiData.HTTP_OK, \
                f"Ожидался статус {ApiData.HTTP_OK}, получен {login_response.status_code}"
        
        with allure.step("Проверить структуру ответа"):
            login_data = login_response.json()
            assert login_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_TRUE
            assert ApiData.KEY_ACCESS_TOKEN in login_data
            assert login_data[ApiData.KEY_USER][ApiData.KEY_EMAIL] == registered_user_success["email"]
            assert login_data[ApiData.KEY_USER][ApiData.KEY_NAME] == registered_user_success["name"]

            
                    