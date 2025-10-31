"""Скрипт для запуска тестов с моками"""
import os
import pytest

def main():
    # Устанавливаем переменную окружения для использования моков
    os.environ['USE_MOCKS'] = 'true'
    
    print("Запуск тестов с мок-API...")
    
    # Запускаем pytest
    pytest.main([
        '-v',
        '--tb=short',
        '--alluredir=allure-results'
    ])

if __name__ == "__main__":
    main()