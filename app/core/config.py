import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

FIRST_ADMIN_NAME=os.getenv("FIRST_ADMIN_USERNAME")
FIRST_ADMIN_EMAIL=os.getenv("FIRST_ADMIN_EMAIL")
FIRST_ADMIN_PASSWORD=os.getenv("FIRST_ADMIN_PASSWORD")
