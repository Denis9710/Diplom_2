import logging


def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('tests.log', encoding='utf-8')
        ]
    )
    return logging.getLogger(__name__)


logger = setup_logging()
