import allure
from helpers.urls import Urls
from helpers.api_data import ApiData
from helpers.mock_responses import MockResponses
from requests.models import Response
import json


class MockStellarBurgersAPI:
    """Мок-класс для работы с API Stellar Burgers (без реальных сетевых запросов)"""
    
    def __init__(self):
        self.urls = Urls()
        self.token = None
        self._mock_data = {}
        self._registered_users = set()
    
    def _create_mock_response(self, status_code, json_data):
        """Создает мок-ответ"""
        response = Response()
        response.status_code = status_code
        response._content = json.dumps(json_data).encode('utf-8')
        return response
    
    @allure.step("Регистрация пользователя (MOCK)")
    def register_user(self, email, password, name):
        """Мок регистрации пользователя"""
        # Исправленная логика проверки обязательных полей
        if not email or not password or not name:
            return self._create_mock_response(
                ApiData.HTTP_BAD_REQUEST, 
                MockResponses.REQUIRED_FIELDS_ERROR
            )
        
        # Исправленная логика проверки существующего пользователя
        if email in self._registered_users:
            return self._create_mock_response(
                ApiData.HTTP_FORBIDDEN,
                MockResponses.USER_EXISTS_ERROR
            )
        
        # Создаем пользователя
        self._registered_users.add(email)
        self._mock_data[email] = {
            "email": email,
            "password": password, 
            "name": name
        }
        
        # Генерируем токен
        token = f"mock_token_{email}_{password}_{name}"
        self.token = token
        
        response_data = MockResponses.SUCCESSFUL_REGISTRATION.copy()
        response_data["accessToken"] = token
        response_data["user"]["email"] = email
        response_data["user"]["name"] = name
        
        return self._create_mock_response(ApiData.HTTP_OK, response_data)
    
    @allure.step("Авторизация пользователя (MOCK)")
    def login_user(self, email, password):
        """Мок авторизации пользователя"""
        # Сбрасываем токен при любой попытке входа
        self.token = None
        
        # Ищем пользователя
        user_data = self._mock_data.get(email)
        # Исправленная логика проверки учетных данных
        if not user_data or user_data["password"] != password:
            return self._create_mock_response(
                ApiData.HTTP_UNAUTHORIZED,
                MockResponses.INVALID_CREDENTIALS_ERROR
            )
        
        # Генерируем токен
        token = f"mock_token_{email}_{password}_{user_data['name']}"
        self.token = token
        
        response_data = MockResponses.SUCCESSFUL_LOGIN.copy()
        response_data["accessToken"] = token
        response_data["user"]["email"] = email
        response_data["user"]["name"] = user_data["name"]
        
        return self._create_mock_response(ApiData.HTTP_OK, response_data)
    
    @allure.step("Удаление пользователя (MOCK)")
    def delete_user(self, token):
        """Мок удаления пользователя"""
        # Исправленная логика проверки токена
        if not token:
            return self._create_mock_response(ApiData.HTTP_BAD_REQUEST, {"success": False})
        
        # Удаляем пользователя по токену
        for email in list(self._mock_data.keys()):
            user_data = self._mock_data[email]
            expected_token = f"mock_token_{email}_{user_data['password']}_{user_data['name']}"
            # Исправленная логика удаления пользователя
            if expected_token == token:
                del self._mock_data[email]
                self._registered_users.discard(email)
                break
        
        self.token = None
        return self._create_mock_response(ApiData.HTTP_OK, {"success": True})
    
    @allure.step("Создание заказа (MOCK)")
    def create_order(self, ingredients, token=None):
        """Мок создания заказа"""
        # Исправленная логика проверки ингредиентов
        if not ingredients:
            return self._create_mock_response(
                ApiData.HTTP_BAD_REQUEST,
                MockResponses.NO_INGREDIENTS_ERROR
            )
        
        # Проверяем валидность ингредиентов
        for ingredient in ingredients:
            # Исправленная логика проверки невалидных ингредиентов
            if ingredient.startswith("invalid_"):
                return self._create_mock_response(
                    ApiData.HTTP_BAD_REQUEST,
                    MockResponses.INVALID_INGREDIENTS_ERROR
                )
        
        response_data = MockResponses.SUCCESSFUL_ORDER.copy()
        response_data["order"]["number"] = len(self._mock_data) + 1000
        
        return self._create_mock_response(ApiData.HTTP_OK, response_data)
    
    @allure.step("Получение списка ингредиентов (MOCK)")
    def get_ingredients(self):
        """Мок получения списка ингредиентов"""
        return self._create_mock_response(ApiData.HTTP_OK, MockResponses.INGREDIENTS_LIST)
    
    @allure.step("Получение валидных ID ингредиентов (MOCK)")
    def get_valid_ingredients(self):
        """Мок получения валидных ID ингредиентов"""
        response = self.get_ingredients()
        response_data = json.loads(response._content.decode('utf-8'))
        ingredients_list = response_data.get("data", [])
        
        valid_ingredients = [
            ingredient["_id"] for ingredient in ingredients_list[:2]
        ]
        return valid_ingredients
    
    