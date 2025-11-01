import random
import string
from faker import Faker


class DataGenerator:
    """Класс для генерации тестовых данных"""
    
    def __init__(self, locale="en_US"):
        self.fake = Faker(locale)
        self.fake.seed_instance(random.randint(1, 1000))
    
    def generate_email(self):
        """Генерация email адреса"""
        return self.fake.email()
    
    def generate_password(self, length=10):
        """Генерация пароля"""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    def generate_name(self):
        """Генерация имени"""
        return self.fake.first_name()
    
    def generate_user_data(self):
        """Генерация полных данных пользователя"""
        return {
            "email": self.generate_email(),
            "password": self.generate_password(),
            "name": self.generate_name()
        }
    
    def generate_invalid_ingredients(self, count=2):
        """Генерация невалидных ID ингредиентов"""
        return [f"invalid_ingredient_{i}" for i in range(1, count + 1)]
    
    def generate_random_string(self, length=10):
        """Генерация случайной строки"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_user_without_email(self):
        """Генерация данных пользователя без email"""
        return {
            "email": "",
            "password": self.generate_password(),
            "name": self.generate_name()
        }
    
    def generate_user_without_password(self):
        """Генерация данных пользователя без пароля"""
        return {
            "email": self.generate_email(),
            "password": "",
            "name": self.generate_name()
        }
    
    def generate_user_without_name(self):
        """Генерация данных пользователя без имени"""
        return {
            "email": self.generate_email(),
            "password": self.generate_password(),
            "name": ""
        }
    
    