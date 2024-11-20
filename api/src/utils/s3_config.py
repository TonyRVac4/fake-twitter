import random
import string
from hashlib import md5
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from tempfile import SpooledTemporaryFile

from types_aiobotocore_s3 import Client
from aiobotocore.session import get_session
from botocore.exceptions import ClientError

from database_models.db_config import ResponseData # noqa
from config import S3_ACCESS_KEY, S3_SECRET_KEY, S3_URL, S3_BUCKET_NANE # noqa


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()
        self.endpoint_url = endpoint_url

    @asynccontextmanager
    async def get_client(self) -> AsyncGenerator[Client, None]:
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload(self, file_obj: SpooledTemporaryFile, filename: str) -> ResponseData:
        hashed_filename = "{hash}.{file_ext}".format(
            hash=S3utils.gen_random_hash(filename),
            file_ext=filename.split(".")[-1],
        )
        try:
            async with self.get_client() as client:
                res = await client.put_object(
                    Bucket=self.bucket_name,
                    Key=hashed_filename,
                    Body=file_obj,
                )
                if res["ResponseMetadata"]["HTTPStatusCode"] != 200:
                    raise ClientError(operation_name="put", error_response=res)

            link: str = S3utils.generate_link(
                url=self.endpoint_url,
                bucket_name=self.bucket_name,
                filename=hashed_filename,
            )
            result, code = {
                "result": True,
                "link": link,
            }, 201
        except ClientError as err:
            result, code = {
                "result": False,
                "error_type": "ClientError",
                "error_message": err,
            }, 500

        return ResponseData(response=result, status_code=code)

    async def delete(self, object_name: str) -> ResponseData:
        try:
            async with self.get_client() as client:
                res = await client.delete_object(Bucket=self.bucket_name, Key=object_name)
                if res["ResponseMetadata"]["HTTPStatusCode"] != 200:
                    raise ClientError(operation_name="delete", error_response=res)
            result, code = {"result": True}, 200
        except ClientError as err:
            result, code = {
                "result": False,
                "error_type": "ClientError",
                "error_message": err,
            }, 500
        return ResponseData(response=result, status_code=code)

    async def delete_multiple(self, media_names: list) -> ResponseData:
        try:
            async with self.get_client() as client:
                for name in media_names:
                    res = await client.delete_object(Bucket=self.bucket_name, Key=name)
                    if res["ResponseMetadata"]["HTTPStatusCode"] != 204:
                        raise ClientError(operation_name="delete", error_response=res)
            result, code = {"result": True}, 200
        except ClientError as err:
            result, code = {
                "result": False,
                "error_type": "ClientError",
                "error_message": err,
            }, 500
        return ResponseData(response=result, status_code=code)


class S3utils:
    @classmethod
    def generate_link(cls, url, bucket_name, filename: str) -> str:
        url = "{url}/{b_name}/{f_name}".format(
            url=url,
            b_name=bucket_name,
            f_name=filename,
        )
        return url

    @classmethod
    def get_name_from_link(cls, link: str) -> str:
        return link.split("/")[-1]

    @classmethod
    def gen_random_hash(cls, filename: str) -> str:
        characters: str = string.ascii_lowercase + string.digits + string.ascii_uppercase
        random_str: str = ''.join(random.choice(characters) for _ in range(16))
        file_name_with_random_str: str = filename + random_str

        result = md5(file_name_with_random_str.encode()).hexdigest()
        return result


async def get_async_s3_client() -> AsyncGenerator[S3Client, None]:
    """Async generator yields main async session for api.

    Yields:

    """
    s3_client = S3Client(
        access_key=S3_ACCESS_KEY,
        secret_key=S3_SECRET_KEY,
        endpoint_url=S3_URL,
        bucket_name=S3_BUCKET_NANE,
    )
    yield s3_client
