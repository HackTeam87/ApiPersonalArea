from starlette.config import Config
config = Config(".env")
# Переменная окружения
DATABASE_URL = config("DATABASE_URL", cast=str, default="")
