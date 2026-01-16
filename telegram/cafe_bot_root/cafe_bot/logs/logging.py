from loguru import logger
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "log_files"
LOG_DIR.mkdir(exist_ok=True)

def is_sales(record) -> bool:
    return record['extra'].get("type") == "sale"

def is_cart(record) -> bool:
    return record['extra'].get("type") == "cart"

def is_payment(record) -> bool:
    return record['extra'].get("type") == "payment"

def is_system(record) -> bool:
    is_system_type = record['extra'].get("type") == "system"
    is_error_type = record['level'].no > 40
    return is_system_type or is_error_type

logger.remove()
logger.add(LOG_DIR / "payments.log", format="{time:YYYY-MM-DD HH:mm:ss} | {message}", rotation="10 MB", compression="zip", filter=is_payment)
logger.add(LOG_DIR / "cart_operations.log", format="{time:YYYY-MM-DD HH:mm:ss} | {message}", rotation="10 MB", compression="zip", filter=is_cart)
logger.add(LOG_DIR / "orders.log", format="{time:YYYY-MM-DD HH:mm:ss} | {message}", rotation="10 MB", compression="zip", filter=is_sales)
logger.add(LOG_DIR / "bot_work.log", format="{time:YYYY-MM-DD HH:mm:ss} | {message}", rotation="1 day", compression="zip", filter=is_system, backtrace=True, diagnose=True)

