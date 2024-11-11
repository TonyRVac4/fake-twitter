import os

from dotenv import load_dotenv

dotenv_path = "{0}/.env".format(os.path.dirname(os.path.dirname(__file__)))

if os.path.exists(dotenv_path):
    load = load_dotenv(dotenv_path)

    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_NAME: str = os.getenv("DB_NAME")

    DATABASE_URL = "postgresql+asyncpg://{user}:{psw}@{host}:{port}".format(
        user=DB_USER,
        psw=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
    )
else:
    raise FileNotFoundError(".env configuration file does not exist")
