import os

required_db_env_vars = ["DB_HOST", "DB_PORT", "DB_PASS", "DB_USER_NAME", "DB_NAME"]
required_s3_env_vars = ["S3_ACCESS_KEY", "S3_SECRET_KEY", "S3_URL", "S3_BUCKET_NANE"]

if all(var in os.environ for var in required_db_env_vars):
    DATABASE_URL = "{driver}://{username}:{db_pass}@{host}:{port}/{db_name}".format(
        driver="postgresql+asyncpg",
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        db_pass=os.environ.get("DB_PASS"),
        username=os.environ.get("DB_USER_NAME"),
        db_name=os.environ.get("DB_NAME"),
    )
else:
    raise EnvironmentError("Database ENV variables not found!")

if all(var in os.environ for var in required_s3_env_vars):
    S3_ACCESS_KEY = os.environ.get("S3_ACCESS_KEY")
    S3_SECRET_KEY = os.environ.get("S3_SECRET_KEY")
    S3_URL = os.environ.get("S3_URL")
    S3_BUCKET_NANE = os.environ.get("S3_BUCKET_NANE")
else:
    raise EnvironmentError("S3 ENV variables not found!")
