class Urls:
    """Класс для хранения URL-адресов API Stellar Burgers"""
    
    # Базовый URL
    BASE_URL = "https://stellarburgers.nomoreparties.site"
    API_PREFIX = "/api"
    
    # Auth endpoints
    REGISTER = f"{BASE_URL}{API_PREFIX}/auth/register"
    LOGIN = f"{BASE_URL}{API_PREFIX}/auth/login"
    USER = f"{BASE_URL}{API_PREFIX}/auth/user"
    LOGOUT = f"{BASE_URL}{API_PREFIX}/auth/logout"
    TOKEN = f"{BASE_URL}{API_PREFIX}/auth/token"
    
    # Order endpoints
    ORDERS = f"{BASE_URL}{API_PREFIX}/orders"
    ORDERS_ALL = f"{BASE_URL}{API_PREFIX}/orders/all"
    
    # Ingredients endpoints
    INGREDIENTS = f"{BASE_URL}{API_PREFIX}/ingredients"
    