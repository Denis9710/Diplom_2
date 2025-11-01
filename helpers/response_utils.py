import json
import allure
from helpers.api_data import ApiData


def parse_response_json(response):
    """Вспомогательная функция для парсинга JSON ответа"""
    try:
        return response.json()
    except (ValueError, json.JSONDecodeError):
        return {"message": f"Invalid JSON response: {response.text}"}


def check_response_status(response, expected_status, operation):
    """Проверка статуса ответа"""
    assert response.status_code == expected_status, f"Не удалось выполнить {operation}: ожидался статус {expected_status}, получен {response.status_code}"


def check_token_exists(token, context):
    """Проверка существования токена"""
    assert token is not None, f"Токен не был получен {context}"
    