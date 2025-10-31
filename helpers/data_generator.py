python
import random
import string
from faker import Faker


class DataGenerator:
    """Класс для генерации тестовых данных"""
    
    def __init__(self, locale="en_US"):
        self.fake = Faker(locale)
        self.fake.seed_instance(random.randint(1, 1000))
    
    def generate_email(self, domain=None):
        """Генерация email адреса"""
        if domain:
            username = self.fake.user_name()
            return f"{username}@{domain}"
        return self.fake.email()
    
    def generate_password(self, length=10, include_special_chars=True):
        """Генерация пароля"""
        if include_special_chars:
            characters = string.ascii_letters + string.digits + "!@#$%^&*"
        else:
            characters = string.ascii_letters + string.digits
        
        return ''.join(random.choice(characters) for _ in range(length))
    
    def generate_name(self):
        """Генерация имени"""
        return self.fake.first_name()
    
    def generate_user_data(self, email=None, password=None, name=None):
        """Генерация полных данных пользователя"""
        return {
            "email": email or self.generate_email(),
            "password": password or self.generate_password(),
            "name": name or self.generate_name()
        }
    
    def generate_invalid_ingredients(self, count=2):
        """Генерация невалидных ID ингредиентов"""
        invalid_ids = []
        for _ in range(count):
            # Генерация случайной строки, похожей на MongoDB ID (24 hex символа)
            fake_id = ''.join(random.choices('0123456789abcdef', k=24))
            invalid_ids.append(fake_id)
        return invalid_ids
    
    def generate_random_string(self, length=10, chars=None):
        """Генерация случайной строки"""
        if chars is None:
            chars = string.ascii_letters + string.digits
        
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_empty_user_data(self, missing_field):
        """Генерация данных пользователя с пропущенным полем"""
        user_data = self.generate_user_data()
        user_data[missing_field] = None
        return user_data


# Создаем экземпляр для удобного импорта
data_generator = DataGenerator()