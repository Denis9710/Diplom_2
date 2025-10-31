"""Мок-ответы для тестирования без реального API сервера"""

class MockResponses:
    """Класс с мок-ответами API Stellar Burgers"""
    
    # Успешная регистрация пользователя
    SUCCESSFUL_REGISTRATION = {
        "success": True,
        "accessToken": "Bearer mock_access_token_12345",
        "refreshToken": "mock_refresh_token_12345", 
        "user": {
            "email": "test@example.com",
            "name": "TestUser"
        }
    }
    
    # Ошибка: пользователь уже существует
    USER_EXISTS_ERROR = {
        "success": False,
        "message": "User already exists"
    }
    
    # Ошибка: обязательные поля отсутствуют
    REQUIRED_FIELDS_ERROR = {
        "success": False, 
        "message": "Email, password and name are required fields"
    }
    
    # Успешный логин
    SUCCESSFUL_LOGIN = {
        "success": True,
        "accessToken": "Bearer mock_access_token_12345",
        "refreshToken": "mock_refresh_token_12345",
        "user": {
            "email": "test@example.com",
            "name": "TestUser"
        }
    }
    
    # Ошибка неверных учетных данных
    INVALID_CREDENTIALS_ERROR = {
        "success": False,
        "message": "email or password are incorrect"
    }
    
    # Список ингредиентов
    INGREDIENTS_LIST = {
        "success": True,
        "data": [
            {
                "_id": "60666c42cc7b410027a1a9b1",
                "name": "Краторная булка N-200i",
                "type": "bun",
                "proteins": 80,
                "fat": 24,
                "carbohydrates": 53,
                "calories": 420,
                "price": 1255,
                "image": "https://code.s3.yandex.net/react/code/bun-02.png",
                "image_mobile": "https://code.s3.yandex.net/react/code/bun-02-mobile.png",
                "image_large": "https://code.s3.yandex.net/react/code/bun-02-large.png",
                "__v": 0
            },
            {
                "_id": "60666c42cc7b410027a1a9b5", 
                "name": "Говяжий метеорит (отбивная)",
                "type": "main",
                "proteins": 800,
                "fat": 800,
                "carbohydrates": 300,
                "calories": 2674,
                "price": 3000,
                "image": "https://code.s3.yandex.net/react/code/meat-04.png",
                "image_mobile": "https://code.s3.yandex.net/react/code/meat-04-mobile.png",
                "image_large": "https://code.s3.yandex.net/react/code/meat-04-large.png",
                "__v": 0
            },
            {
                "_id": "60666c42cc7b410027a1a9b6",
                "name": "Биокотлета из марсианской Магнолии",
                "type": "main", 
                "proteins": 420,
                "fat": 142,
                "carbohydrates": 242,
                "calories": 4242,
                "price": 424,
                "image": "https://code.s3.yandex.net/react/code/meat-01.png",
                "image_mobile": "https://code.s3.yandex.net/react/code/meat-01-mobile.png",
                "image_large": "https://code.s3.yandex.net/react/code/meat-01-large.png",
                "__v": 0
            }
        ]
    }
    
    # Успешное создание заказа
    SUCCESSFUL_ORDER = {
        "success": True,
        "name": "Флюоресцентный spicy бургер",
        "order": {
            "number": 12345,
            "ingredients": [
                {
                    "_id": "60666c42cc7b410027a1a9b1",
                    "name": "Краторная булка N-200i",
                    "type": "bun",
                    "proteins": 80,
                    "fat": 24,
                    "carbohydrates": 53,
                    "calories": 420,
                    "price": 1255,
                    "image": "https://code.s3.yandex.net/react/code/bun-02.png",
                    "image_mobile": "https://code.s3.yandex.net/react/code/bun-02-mobile.png",
                    "image_large": "https://code.s3.yandex.net/react/code/bun-02-large.png",
                    "__v": 0
                },
                {
                    "_id": "60666c42cc7b410027a1a9b5",
                    "name": "Говяжий метеорит (отбивная)",
                    "type": "main",
                    "proteins": 800,
                    "fat": 800,
                    "carbohydrates": 300,
                    "calories": 2674,
                    "price": 3000,
                    "image": "https://code.s3.yandex.net/react/code/meat-04.png",
                    "image_mobile": "https://code.s3.yandex.net/react/code/meat-04-mobile.png",
                    "image_large": "https://code.s3.yandex.net/react/code/meat-04-large.png",
                    "__v": 0
                }
            ],
            "_id": "1234567890",
            "status": "done",
            "createdAt": "2024-01-01T00:00:00.000Z",
            "updatedAt": "2024-01-01T00:00:00.000Z",
            "number": 12345
        }
    }
    
    # Ошибка: ингредиенты не предоставлены
    NO_INGREDIENTS_ERROR = {
        "success": False,
        "message": "Ingredient ids must be provided"
    }
    
    # Ошибка: неверные ингредиенты
    INVALID_INGREDIENTS_ERROR = {
        "success": False, 
        "message": "One or more ids provided are incorrect"
    }
    