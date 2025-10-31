import requests
import allure
from helpers.urls import Urls
from helpers.api_data import ApiData


class StellarBurgersAPI:
    """Класс для работы с API Stellar Burgers"""
    
    def __init__(self):
        self.urls = Urls()
        self.session = requests.Session()
        self.token = None
    
    @allure.step("Регистрация пользователя")
    def register_user(self, email, password, name):
        """Регистрация нового пользователя"""
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        
        response = self.session.post(self.urls.REGISTER, json=payload)
        return response
    
    @allure.step("Авторизация пользователя")
    def login_user(self, email, password):
        """Авторизация пользователя"""
        payload = {
            "email": email,
            "password": password
        }
        
        response = self.session.post(self.urls.LOGIN, json=payload)
        
        # Сохраняем токен, но не делаем условий - проверка в тестах
        response_data = response.json()
        self.token = response_data.get(ApiData.KEY_ACCESS_TOKEN)
        
        return response
    
    @allure.step("Удаление пользователя")
    def delete_user(self, token):
        """Удаление пользователя"""
        headers = {"Authorization": token}
        response = self.session.delete(self.urls.USER, headers=headers)
        return response
    
    @allure.step("Создание заказа")
    def create_order(self, ingredients, token=None):
        """Создание заказа"""
        headers = {}
        if token:
            headers["Authorization"] = token
        
        payload = {
            "ingredients": ingredients
        }
        
        response = self.session.post(self.urls.ORDERS, json=payload, headers=headers)
        return response
    
    @allure.step("Получение списка ингредиентов")
    def get_ingredients(self):
        """Получение списка ингредиентов"""
        response = self.session.get(self.urls.INGREDIENTS)
        return response
    
    @allure.step("Получение валидных ID ингредиентов")
    def get_valid_ingredients(self):
        """Получение валидных ID ингредиентов"""
        response = self.get_ingredients()
        response_data = response.json()
        ingredients_list = response_data.get(ApiData.KEY_DATA, [])
        
        # Берем первые 2 ингредиента без условий
        valid_ingredients = [ingredient[ApiData.KEY_ID] for ingredient in ingredients_list[:2]]
        return valid_ingredients