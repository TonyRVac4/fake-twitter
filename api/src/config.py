import os
from dotenv import load_dotenv

dotenv_path = os.path.join('/'.join(os.path.dirname(__file__).split("/")[:-1]), '.env')
if os.path.exists(dotenv_path):
    a = load_dotenv(dotenv_path)

    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_NAME: str = os.getenv("DB_NAME")

    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}"
else:
    raise Exception(".env configuration file does not exist")
