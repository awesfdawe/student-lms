import aioboto3
from app.core.config import settings

session = aioboto3.Session()
s3_client = None

async def init_storage():
    global s3_client
    s3_client = await session.client(
        's3',
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name=settings.S3_REGION
    ).__aenter__()

async def close_storage():
    global s3_client
    if s3_client:
        await s3_client.__aexit__(None, None, None)

async def upload_file(key, data, content_type="application/octet-stream"):
    await s3_client.put_object(
        Bucket=settings.S3_BUCKET,
        Key=key,
        Body=data,
        ContentType=content_type
    )

async def download_file(key):
    response = await s3_client.get_object(
        Bucket=settings.S3_BUCKET,
        Key=key
    )
    return await response["Body"].read()

async def delete_file(key):
    await s3_client.delete_object(
        Bucket=settings.S3_BUCKET,
        Key=key
    )

async def generate_presigned_url(key, expires_in=3600):
    return await s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.S3_BUCKET,
            "Key": key
        },
        ExpiresIn=expires_in
    )
