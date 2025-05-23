# app/core/logger.py
import logging
from datetime import datetime
import os

# Make sure log directory exists
os.makedirs("log", exist_ok=True)

# Create a logger instance
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(module)s : %(funcName)s : %(message)s",
    "%Y-%m-%d %H:%M:%S"
)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# File handler
file_handler = logging.FileHandler(f"log/pugzhavi-uwsgi-{datetime.today().date()}.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Avoid duplicate handlers if re-imported
if not logger.hasHandlers():
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

# Silence other loggers
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("fastapi").setLevel(logging.WARNING)
logging.getLogger("fastapi.error").setLevel(logging.WARNING)
logging.getLogger("fastapi.access").setLevel(logging.WARNING)
