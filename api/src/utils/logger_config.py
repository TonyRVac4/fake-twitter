import logging
import os

os.chdir(os.path.dirname(os.path.dirname(__file__)))

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

root_logger = logging.getLogger()
api_logger = logging.getLogger("api")
orm_logger = logging.getLogger("orm")
s3_logger = logging.getLogger("s3")

root_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/logs.log", mode="a")
console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(name)s | %(asctime)s | %(levelname)s | %(message)s",  # noqa: WPS323
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

root_logger.addHandler(file_handler)
