from os import getenv
from dotenv import load_dotenv


load_dotenv()

BASE_PREFIX = "/api"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

DB_URL = getenv("DB_URL")
SECRET_KEY = getenv("SECRET_KEY")
