import pytest
import allure
import os
from helpers.api_client import StellarBurgersAPI
from helpers.mock_api_client import MockStellarBurgersAPI
from helpers.data_generator import DataGenerator
from helpers.api_data import ApiData
from helpers.response_utils import parse_response_json, check_response_status, check_token_exists
from helpers.logger import logger

# Определяем, использовать ли моки
USE_MOCKS = os.getenv('USE_MOCKS', 'true').lower() == 'true'


@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    client_class = MockStellarBurgersAPI if USE_MOCKS else StellarBurgersAPI
    return client_class()


@pytest.fixture
def data_generator():
    """Фикстура для генератора тестовых данных"""
    return DataGenerator()


@pytest.fixture
def user_credentials(data_generator):
    """Фикстура для генерации данных пользователя"""
    return data_generator.generate_user_data()


@pytest.fixture
def registered_user_success(api_client, user_credentials):
    """Фикстура для успешно созданного пользователя с cleanup"""
    token = None
    try:
        response = api_client.register_user(
            email=user_credentials["email"],
            password=user_credentials["password"],
            name=user_credentials["name"]
        )
        
        check_response_status(response, ApiData.HTTP_OK, "создания пользователя")
        
        response_data = parse_response_json(response)
        token = response_data.get(ApiData.KEY_ACCESS_TOKEN)
        check_token_exists(token, "при регистрации")
        
        user_data = {
            **user_credentials,
            "token": token,
            "response": response
        }
        
        yield user_data
        
    finally:
        token and api_client.delete_user(token)


@pytest.fixture
def authorized_user_success(api_client, user_credentials):
    """Фикстура для успешно авторизованного пользователя"""
    token = None
    try:
        response = api_client.register_user(
            email=user_credentials["email"],
            password=user_credentials["password"],
            name=user_credentials["name"]
        )
        
        check_response_status(response, ApiData.HTTP_OK, "создания пользователя")
        
        login_response = api_client.login_user(
            email=user_credentials["email"],
            password=user_credentials["password"]
        )
        
        check_response_status(login_response, ApiData.HTTP_OK, "авторизации пользователя")
        
        token = api_client.token
        check_token_exists(token, "при авторизации")
        
        user_data = {
            **user_credentials,
            "token": token
        }
        
        yield user_data
        
    finally:
        token and api_client.delete_user(token)


@pytest.fixture
def existing_user_credentials(registered_user_success):
    """Фикстура для данных существующего пользователя"""
    return {
        "email": registered_user_success["email"],
        "password": registered_user_success["password"],
        "name": registered_user_success["name"]
    }


@pytest.fixture
def ingredients_list(api_client):
    """Фикстура для получения списка ингредиентов"""
    response = api_client.get_ingredients()
    check_response_status(response, ApiData.HTTP_OK, "получения ингредиентов")
    
    response_data = parse_response_json(response)
    ingredients_data = response_data.get(ApiData.KEY_DATA, [])
    return ingredients_data


def pytest_configure(config):
    """Конфигурация pytest маркеров"""
    config.addinivalue_line("markers", "smoke: Маркер для smoke тестов")
    config.addinivalue_line("markers", "regression: Маркер для regression тестов")
    config.addinivalue_line("markers", "api: Маркер для API тестов")
    config.addinivalue_line("markers", "positive: Маркер для позитивных тестов")
    config.addinivalue_line("markers", "negative: Маркер для негативных тестов")
    config.addinivalue_line("markers", "real_api: Маркер для тестов с реальным API")
    config.addinivalue_line("markers", "mock_api: Маркер для тестов с мок-API")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для интеграции с Allure"""
    outcome = yield
    rep = outcome.get_result()
    
    rep.when == "call" and hasattr(item, 'callspec') and item.callspec.params and allure.dynamic.title(f"{item.originalname} [{item.callspec.params}]")


@pytest.fixture(autouse=True)
def add_allure_environment(request):
    """Автоматическое добавление информации в Allure"""
    allure.dynamic.epic("Stellar Burgers API")
    allure.dynamic.feature(request.module.__name__.replace('test_', '').replace('_', ' ').title())
    
    api_tag = "mock_api" if USE_MOCKS else "real_api"
    allure.dynamic.tag(api_tag)
    
    marker_tags = {
        "smoke": "smoke",
        "regression": "regression",
        "positive": "positive", 
        "negative": "negative",
        "real_api": "real_api",
        "mock_api": "mock_api"
    }
    
    for marker in request.node.own_markers:
        marker.name in marker_tags and allure.dynamic.tag(marker_tags[marker.name])


def pytest_collection_modifyitems(config, items):
    """Модификация коллекции тестов в зависимости от типа API"""
    skip_marker = "real_api" if USE_MOCKS else "mock_api"
    skip_reason = "Тест требует реального API" if USE_MOCKS else "Тест предназначен только для мок-API"
    
    skip_api = pytest.mark.skip(reason=skip_reason)
    for item in items:
        skip_marker in [marker.name for marker in item.own_markers] and item.add_marker(skip_api)


def pytest_sessionstart(session):
    """Действия при запуске сессии тестов"""
    api_type = "МОК-API" if USE_MOCKS else "РЕАЛЬНОГО API"
    logger.info("=" * 60)
    logger.info("ЗАПУСК ТЕСТОВ С %s", api_type)
    logger.info("=" * 60)


def pytest_sessionfinish(session, exitstatus):
    """Действия при завершении сессии тестов"""
    api_type = "МОК-API" if USE_MOCKS else "РЕАЛЬНОГО API"
    logger.info("=" * 60)
    logger.info("ТЕСТЫ С %s ЗАВЕРШЕНЫ", api_type)
    logger.info("=" * 60)

    