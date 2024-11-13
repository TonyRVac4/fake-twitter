import os

if "DATABASE_URL" in os.environ:
    DATABASE_URL = os.environ.get("DATABASE_URL")
else:
    raise EnvironmentError("DATABASE_URL variable not found")
