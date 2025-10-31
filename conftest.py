import pytest
import allure
import json
import os
from helpers.api_client import StellarBurgersAPI
from helpers.mock_api_client import MockStellarBurgersAPI
from helpers.data_generator import DataGenerator
from helpers.api_data import ApiData

# Определяем, использовать ли моки
USE_MOCKS = os.getenv('USE_MOCKS', 'true').lower() == 'true'


@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    return MockStellarBurgersAPI() if USE_MOCKS else StellarBurgersAPI()


@pytest.fixture
def data_generator():
    """Фикстура для генератора тестовых данных"""
    return DataGenerator()


@pytest.fixture
def user_credentials(data_generator):
    """Фикстура для генерации данных пользователя"""
    return data_generator.generate_user_data()


def _parse_response_json(response):
    """Вспомогательная функция для парсинга JSON ответа"""
    try:
        return response.json()
    except (ValueError, json.JSONDecodeError):
        return {"message": f"Invalid JSON response: {response.text}"}


@pytest.fixture
def registered_user_success(api_client, user_credentials):
    """Фикстура для успешно созданного пользователя с cleanup"""
    token = None
    try:
        with allure.step("Создать пользователя через API"):
            response = api_client.register_user(
                email=user_credentials["email"],
                password=user_credentials["password"],
                name=user_credentials["name"]
            )
        
        _check_response_status(response, ApiData.HTTP_OK, "создания пользователя")
        
        response_data = _parse_response_json(response)
        token = response_data.get(ApiData.KEY_ACCESS_TOKEN)
        _check_token_exists(token, "при регистрации")
        
        user_data = {
            **user_credentials,
            "token": token,
            "response": response
        }
        
        yield user_data
        
    finally:
        if token:
            with allure.step("Удалить созданного пользователя"):
                api_client.delete_user(token)


@pytest.fixture
def authorized_user_success(api_client, user_credentials):
    """Фикстура для успешно авторизованного пользователя"""
    token = None
    try:
        with allure.step("Создать и авторизовать пользователя"):
            # Создаем пользователя
            response = api_client.register_user(
                email=user_credentials["email"],
                password=user_credentials["password"],
                name=user_credentials["name"]
            )
            
            _check_response_status(response, ApiData.HTTP_OK, "создания пользователя")
            
            # Авторизуемся
            login_response = api_client.login_user(
                email=user_credentials["email"],
                password=user_credentials["password"]
            )
            
            _check_response_status(login_response, ApiData.HTTP_OK, "авторизации пользователя")
            
            token = api_client.token
            _check_token_exists(token, "при авторизации")
            
            user_data = {
                **user_credentials,
                "token": token
            }
            
            yield user_data
            
    finally:
        if token:
            with allure.step("Удалить пользователя"):
                api_client.delete_user(token)


@pytest.fixture
def existing_user_credentials(registered_user_success):
    """Фикстура для данных существующего пользователя"""
    return {
        "email": registered_user_success["email"],
        "password": registered_user_success["password"],
        "name": registered_user_success["name"]
    }


@pytest.fixture
def ingredients_list():
    """Фикстура для получения списка ингредиентов"""
    if USE_MOCKS:
        client = MockStellarBurgersAPI()
    else:
        client = StellarBurgersAPI()
    
    with allure.step("Получить список ингредиентов"):
        response = client.get_ingredients()
    
    _check_response_status(response, ApiData.HTTP_OK, "получения ингредиентов")
    
    response_data = _parse_response_json(response)
    ingredients_data = response_data.get(ApiData.KEY_DATA, [])
    return ingredients_data


@pytest.fixture
def valid_ingredients(ingredients_list):
    """Фикстура для получения валидных ID ингредиентов"""
    if len(ingredients_list) < 2:
        pytest.skip("Недостаточно ингредиентов для теста (нужно минимум 2)")
    return [ingredient[ApiData.KEY_ID] for ingredient in ingredients_list[:2]]


@pytest.fixture
def invalid_ingredients(data_generator):
    """Фикстура для генерации невалидных ID ингредиентов"""
    return data_generator.generate_invalid_ingredients()


@pytest.fixture
def empty_ingredients():
    """Фикстура для пустого списка ингредиентов"""
    return []


@pytest.fixture
def mock_ingredients():
    """Фикстура с мок-ингредиентами для тестов"""
    return [
        "60666c42cc7b410027a1a9b1",
        "60666c42cc7b410027a1a9b5", 
        "60666c42cc7b410027a1a9b6"
    ]


# Вспомогательные функции для проверок
def _check_response_status(response, expected_status, operation):
    """Проверка статуса ответа"""
    assert response.status_code == expected_status, f"Не удалось выполнить {operation}: ожидался статус {expected_status}, получен {response.status_code}"


def _check_token_exists(token, context):
    """Проверка существования токена"""
    assert token is not None, f"Токен не был получен {context}"


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
    
    if rep.when == "call" and hasattr(item, 'callspec'):
        params = item.callspec.params
        if params:
            allure.dynamic.title(f"{item.originalname} [{params}]")


@pytest.fixture(autouse=True)
def add_allure_environment(request):
    """Автоматическое добавление информации в Allure"""
    allure.dynamic.epic("Stellar Burgers API")
    allure.dynamic.feature(request.module.__name__.replace('test_', '').replace('_', ' ').title())
    
    # Добавляем информацию о типе API
    if USE_MOCKS:
        allure.dynamic.tag("mock_api")
    else:
        allure.dynamic.tag("real_api")
    
    # Добавляем теги на основе маркеров
    marker_tags = {
        "smoke": "smoke",
        "regression": "regression",
        "positive": "positive", 
        "negative": "negative",
        "real_api": "real_api",
        "mock_api": "mock_api"
    }
    
    for marker in request.node.own_markers:
        if marker.name in marker_tags:
            allure.dynamic.tag(marker_tags[marker.name])


def pytest_collection_modifyitems(config, items):
    """Модификация коллекции тестов в зависимости от типа API"""
    if USE_MOCKS:
        # При использовании моков пропускаем тесты, помеченные как real_api
        skip_real_api = pytest.mark.skip(reason="Тест требует реального API")
        for item in items:
            if "real_api" in [marker.name for marker in item.own_markers]:
                item.add_marker(skip_real_api)
    else:
        # При использовании реального API пропускаем тесты, помеченные как mock_api
        skip_mock_api = pytest.mark.skip(reason="Тест предназначен только для мок-API")
        for item in items:
            if "mock_api" in [marker.name for marker in item.own_markers]:
                item.add_marker(skip_mock_api)


# Запуск тестов
def pytest_sessionstart(session):
    """Действия при запуске сессии тестов"""
    print("\n" + "="*60)
    print("🚀 ЗАПУСК ТЕСТОВ С МОК-API" if USE_MOCKS else "🌐 ЗАПУСК ТЕСТОВ С РЕАЛЬНЫМ API")
    print("="*60)


def pytest_sessionfinish(session, exitstatus):
    """Действия при завершении сессии тестов"""
    print("\n" + "="*60)
    print("✅ ТЕСТЫ С МОК-API ЗАВЕРШЕНЫ" if USE_MOCKS else "✅ ТЕСТЫ С РЕАЛЬНЫМ API ЗАВЕРШЕНЫ")
    print("="*60)

    