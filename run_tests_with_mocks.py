import os
import pytest
from helpers.logger import logger

def main():
    # Устанавливаем переменную окружения для использования моков
    os.environ['USE_MOCKS'] = 'true'
    
    logger.info("Запуск тестов с мок-API...")
    
    # Запускаем pytest
    pytest.main([
        '-v',
        '--tb=short',
        '--alluredir=allure-results'
    ])

if __name__ == "__main__":
    main()