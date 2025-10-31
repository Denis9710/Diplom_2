class ApiData:
    """Класс для хранения констант API Stellar Burgers"""
    
    # HTTP status codes
    HTTP_OK = 200
    HTTP_CREATED = 201
    HTTP_BAD_REQUEST = 400
    HTTP_UNAUTHORIZED = 401
    HTTP_FORBIDDEN = 403
    HTTP_NOT_FOUND = 404
    HTTP_INTERNAL_ERROR = 500
    
    # Response messages
    SUCCESS_TRUE = True
    SUCCESS_FALSE = False
    
    # Error messages
    USER_EXISTS_MESSAGE = "User already exists"
    REQUIRED_FIELDS_MESSAGE = "Email, password and name are required fields"
    INVALID_CREDENTIALS_MESSAGE = "email or password are incorrect"
    NO_INGREDIENTS_MESSAGE = "Ingredient ids must be provided"
    INVALID_INGREDIENTS_MESSAGE = "One or more ids provided are incorrect"
    
    # Response keys
    KEY_SUCCESS = "success"
    KEY_ACCESS_TOKEN = "accessToken"
    KEY_REFRESH_TOKEN = "refreshToken"
    KEY_USER = "user"
    KEY_EMAIL = "email"
    KEY_PASSWORD = "password"
    KEY_NAME = "name"
    KEY_MESSAGE = "message"
    KEY_ORDER = "order"
    KEY_NUMBER = "number"
    KEY_INGREDIENTS = "ingredients"
    KEY_DATA = "data"
    KEY_ID = "_id"
    
    # Test data constants
    MIN_PASSWORD_LENGTH = 6
    MAX_PASSWORD_LENGTH = 20
    