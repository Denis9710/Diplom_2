import allure
import pytest
from helpers.api_data import ApiData


@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestCreateOrder:
    
    @allure.title("Создание заказа с авторизацией")
    @allure.description("Тест проверяет успешное создание заказа авторизованным пользователем")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_create_order_with_auth_success(self, api_client, authorized_user, valid_ingredients):
        with allure.step("Создать заказ с ингредиентами"):
            response = api_client.create_order(
                ingredients=valid_ingredients,
                token=authorized_user["token"]
            )
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == ApiData.HTTP_OK, \
                f"Ожидался статус {ApiData.HTTP_OK}, получен {response.status_code}"
        
        with allure.step("Проверить структуру ответа"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_TRUE
            assert ApiData.KEY_ORDER in response_data
            assert ApiData.KEY_NUMBER in response_data[ApiData.KEY_ORDER]
    
    @allure.title("Создание заказа без авторизации")
    @allure.description("Тест проверяет создание заказа без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    def test_create_order_without_auth_success(self, api_client, valid_ingredients):
        with allure.step("Создать заказ без авторизации"):
            response = api_client.create_order(
                ingredients=valid_ingredients,
                token=None
            )
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == ApiData.HTTP_OK, \
                f"Ожидался статус {ApiData.HTTP_OK}, получен {response.status_code}"
        
        with allure.step("Проверить структуру ответа"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_TRUE
            assert ApiData.KEY_ORDER in response_data
    
    @allure.title("Создание заказа с ингредиентами")
    @allure.description("Тест проверяет успешное создание заказа с валидными ингредиентами")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    def test_create_order_with_ingredients_success(self, api_client, authorized_user, valid_ingredients):
        with allure.step("Создать заказ с ингредиентами"):
            response = api_client.create_order(
                ingredients=valid_ingredients,
                token=authorized_user["token"]
            )
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == ApiData.HTTP_OK, \
                f"Ожидался статус {ApiData.HTTP_OK}, получен {response.status_code}"
        
        with allure.step("Проверить наличие ингредиентов в заказе"):
            response_data = response.json()
            order_data = response_data[ApiData.KEY_ORDER]
            assert ApiData.KEY_INGREDIENTS in order_data
            assert len(order_data[ApiData.KEY_INGREDIENTS]) > 0
    
    @allure.title("Создание заказа без ингредиентов")
    @allure.description("Тест проверяет ошибку при создании заказа без ингредиентов")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_create_order_without_ingredients_error(self, api_client, authorized_user):
        with allure.step("Создать заказ без ингредиентов"):
            response = api_client.create_order(
                ingredients=[],
                token=authorized_user["token"]
            )
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == ApiData.HTTP_BAD_REQUEST, \
                f"Ожидался статус {ApiData.HTTP_BAD_REQUEST}, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE
            assert ApiData.NO_INGREDIENTS_MESSAGE in response_data.get(ApiData.KEY_MESSAGE, "")
    
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @allure.description("Тест проверяет ошибку при создании заказа с невалидными ингредиентами")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_create_order_invalid_ingredients_error(self, api_client, authorized_user, invalid_ingredients):
        with allure.step("Создать заказ с невалидными ингредиентами"):
            response = api_client.create_order(
                ingredients=invalid_ingredients,
                token=authorized_user["token"]
            )
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code in [ApiData.HTTP_BAD_REQUEST, ApiData.HTTP_INTERNAL_ERROR], \
                f"Ожидался статус {ApiData.HTTP_BAD_REQUEST} или {ApiData.HTTP_INTERNAL_ERROR}, получен {response.status_code}"
        
        with allure.step("Проверить наличие ошибки в ответе"):
            response_data = response.json()
            assert response_data[ApiData.KEY_SUCCESS] == ApiData.SUCCESS_FALSE
            