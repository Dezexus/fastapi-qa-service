import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
import json
from datetime import datetime, timezone, timedelta
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        # Получаем текущее время в Московском часовом поясе (UTC+3)
        moscow_tz = timezone(timedelta(hours=3))
        timestamp = datetime.now(moscow_tz).isoformat().replace('+03:00', 'Z')

        log_data: Dict[str, Any] = {
            "timestamp": timestamp,
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # Добавляем дополнительные поля, если есть
        if hasattr(record, 'extra_data'):
            log_data.update(record.extra_data)

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


def setup_logging() -> None:

    # Создаем директорию для логов если ее нет
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Основной логгер приложения
    logger = logging.getLogger("qa_service")
    logger.setLevel(logging.INFO)

    # Предотвращаем дублирование логов
    logger.propagate = False

    # Если хендлеры уже настроены, выходим
    if logger.handlers:
        return

    # Форматтер для консоли
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Форматтер для файлов (JSON)
    file_formatter = JSONFormatter()

    # Консольный хендлер
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Файловый хендлер с ротацией
    file_handler = RotatingFileHandler(
        filename=log_dir / "qa_service.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)

    # Хендлер для ошибок
    error_handler = RotatingFileHandler(
        filename=log_dir / "qa_service_errors.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)

    # Добавляем хендлеры к логгеру
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"qa_service.{name}")


# Инициализация логирования при импорте модуля
setup_logging()