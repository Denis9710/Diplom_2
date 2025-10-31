import requests
import allure
from requests.models import Response
from helpers.urls import Urls
from helpers.api_data import ApiData


class StellarBurgersAPI:
    """Класс для работы с API Stellar Burgers"""
    
    def __init__(self):
        self.urls = Urls()
        self.session = requests.Session()
        self.token = None
    
    def _handle_request(self, method, url, **kwargs):
        """Обработчик запросов с обработкой исключений"""
        try:
            if 'timeout' not in kwargs:
                kwargs['timeout'] = 10
            response = self.session.request(method, url, **kwargs)
            return response
        except requests.RequestException as e:
            # Создаем mock response с ошибкой сети
            response = Response()
            response.status_code = ApiData.NETWORK_ERROR
            response._content = str.encode(f"Network error: {e}")
            return response
    
    @allure.step("Регистрация пользователя")
    def register_user(self, email, password, name):
        """Регистрация нового пользователя"""
        payload = {
            "email": email or "",
            "password": password or "",
            "name": name or ""
        }
        
        return self._handle_request('POST', self.urls.REGISTER, json=payload)
    
    @allure.step("Авторизация пользователя")
    def login_user(self, email, password):
        """Авторизация пользователя"""
        payload = {
            "email": email,
            "password": password
        }
        
        response = self._handle_request('POST', self.urls.LOGIN, json=payload)
        
        # Сбрасываем токен при любой ошибке
        self.token = None
        
        if response.status_code == ApiData.HTTP_OK:
            try:
                response_data = response.json()
                self.token = response_data.get(ApiData.KEY_ACCESS_TOKEN)
            except ValueError:
                pass  # Токен остается None
        
        return response
    
    @allure.step("Удаление пользователя")
    def delete_user(self, token):
        """Удаление пользователя"""
        if not token:
            return None
            
        headers = {"Authorization": f"Bearer {token}"}
        return self._handle_request('DELETE', self.urls.USER, headers=headers)
    
    @allure.step("Создание заказа")
    def create_order(self, ingredients, token=None):
        """Создание заказа"""
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        payload = {
            "ingredients": ingredients
        }
        
        return self._handle_request('POST', self.urls.ORDERS, json=payload, headers=headers)
    
    @allure.step("Получение списка ингредиентов")
    def get_ingredients(self):
        """Получение списка ингредиентов"""
        return self._handle_request('GET', self.urls.INGREDIENTS)
    
    @allure.step("Получение валидных ID ингредиентов")
    def get_valid_ingredients(self):
        """Получение валидных ID ингредиентов"""
        response = self.get_ingredients()
        
        if response.status_code != ApiData.HTTP_OK:
            return []
        
        try:
            response_data = response.json()
            ingredients_list = response_data.get(ApiData.KEY_DATA, [])
            
            valid_ingredients = [
                ingredient[ApiData.KEY_ID] for ingredient in ingredients_list[:2]
            ]
            return valid_ingredients
        except (ValueError, KeyError):
            return []
        
        