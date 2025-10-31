import pytest
import allure
from helpers.api_client import StellarBurgersAPI
from helpers.data_generator import DataGenerator
from helpers.api_data import ApiData


@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    return StellarBurgersAPI()


@pytest.fixture
def data_generator():
    """Фикстура для генератора тестовых данных"""
    return DataGenerator()


@pytest.fixture
def user_credentials(data_generator):
    """Фикстура для генерации данных пользователя"""
    return data_generator.generate_user_data()


@pytest.fixture
def registered_user(api_client, user_credentials):
    """Фикстура для успешно созданного пользователя с cleanup"""
    with allure.step("Создать пользователя через API"):
        response = api_client.register_user(
            email=user_credentials["email"],
            password=user_credentials["password"],
            name=user_credentials["name"]
        )
    
    assert response.status_code == ApiData.HTTP_OK, f"Не удалось создать пользователя: {response.text}"
    
    response_data = response.json()
    token = response_data.get(ApiData.KEY_ACCESS_TOKEN)
    user_data = {
        **user_credentials,
        "token": token,
        "response": response
    }
    
    yield user_data
    
    with allure.step("Удалить созданного пользователя"):
        api_client.delete_user(token)


@pytest.fixture
def authorized_user(api_client, registered_user):
    """Фикстура для авторизованного пользователя"""
    with allure.step("Авторизовать пользователя"):
        login_response = api_client.login_user(
            email=registered_user["email"],
            password=registered_user["password"]
        )
    
    assert login_response.status_code == ApiData.HTTP_OK, "Не удалось авторизовать пользователя"
    
    return {
        **registered_user,
        "token": api_client.token
    }


@pytest.fixture
def existing_user_credentials(registered_user):
    """Фикстура для данных существующего пользователя"""
    return {
        "email": registered_user["email"],
        "password": registered_user["password"],
        "name": registered_user["name"]
    }


@pytest.fixture(scope="session")
def ingredients_list(api_client):
    """Фикстура для получения списка ингредиентов"""
    with allure.step("Получить список ингредиентов"):
        response = api_client.get_ingredients()
    
    assert response.status_code == ApiData.HTTP_OK, f"Не удалось получить ингредиенты: {response.status_code}"
    
    response_data = response.json()
    ingredients_data = response_data.get(ApiData.KEY_DATA, [])
    return ingredients_data


@pytest.fixture
def valid_ingredients(ingredients_list):
    """Фикстура для получения валидных ID ингредиентов"""
    assert len(ingredients_list) >= 2, "Недостаточно ингредиентов для теста"
    return [ingredient[ApiData.KEY_ID] for ingredient in ingredients_list[:2]]


@pytest.fixture
def invalid_ingredients(data_generator):
    """Фикстура для генерации невалидных ID ингредиентов"""
    return data_generator.generate_invalid_ingredients()


@pytest.fixture
def empty_ingredients():
    """Фикстура для пустого списка ингредиентов"""
    return []


def pytest_configure(config):
    """Конфигурация pytest маркеров"""
    config.addinivalue_line("markers", "smoke: Маркер для smoke тестов")
    config.addinivalue_line("markers", "regression: Маркер для regression тестов")
    config.addinivalue_line("markers", "api: Маркер для API тестов")
    config.addinivalue_line("markers", "positive: Маркер для позитивных тестов")
    config.addinivalue_line("markers", "negative: Маркер для негативных тестов")


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
    
    markers = [marker.name for marker in request.node.own_markers]
    if "smoke" in markers:
        allure.dynamic.tag("smoke")
    if "regression" in markers:
        allure.dynamic.tag("regression")
    if "positive" in markers:
        allure.dynamic.tag("positive")
    if "negative" in markers:
        allure.dynamic.tag("negative")