from pathlib import Path
import os
from dotenv import load_dotenv

# Base directory (project root)
BASE_DIR = Path(__file__).resolve().parent
ENV = os.getenv("ENV", "development")

print("BAse Path ==> : " , BASE_DIR)

# Absolute path to the env file
dotenv_path = BASE_DIR / f".env.{ENV}"

if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(f"Environment file {dotenv_path} not found.")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in environment variables.")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
DB_ECHO = os.getenv("DB_ECHO", "False").lower() == "true"
