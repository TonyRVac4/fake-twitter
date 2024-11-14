import os

required_env_vars = ["DB_HOST", "DB_PORT", "DB_PASS", "DB_USER_NAME"]

if all(var in os.environ for var in required_env_vars):
    DATABASE_URL = "postgresql+asyncpg://{username}:{db_pass}@{host}:{port}".format(
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        db_pass=os.environ.get("DB_PASS"),
        username=os.environ.get("DB_USER_NAME"),
    )
else:
    raise EnvironmentError("ENV variables not found!")
