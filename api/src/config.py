import os

from dotenv import load_dotenv

required_db_env_vars = ["DB_HOST", "DB_PORT", "DB_PASS", "DB_USER_NAME", "DB_NAME"]
required_s3_env_vars = ["S3_ACCESS_KEY", "S3_SECRET_KEY", "S3_URL", "S3_BUCKET_NANE"]

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

if all(var in os.environ for var in required_db_env_vars):
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_PASS = os.getenv("DB_PASS")
    DB_USER_NAME = os.getenv("DB_USER_NAME")
    DB_NAME = os.getenv("DB_NAME")
    DATABASE_URL = "{driver}://{username}:{db_pass}@{host}:{port}/{db_name}".format(
        driver="postgresql+asyncpg",
        host=DB_HOST,
        port=DB_PORT,
        db_pass=DB_PASS,
        username=DB_USER_NAME,
        db_name=DB_NAME,
    )
else:
    raise EnvironmentError("Database ENV variables not found!")

if all(var in os.environ for var in required_s3_env_vars):
    S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
    S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
    S3_URL = os.getenv("S3_URL")
    S3_BUCKET_NANE = os.getenv("S3_BUCKET_NANE")
else:
    raise EnvironmentError("S3 ENV variables not found!")
