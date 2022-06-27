from datetime import timedelta
import os

databaseUrl = os.environ["DATABASE_URL"]
redisUrl = os.environ["REDIS_URL"]


class Configuration():
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{databaseUrl}/products"
    REDIS_URL = redisUrl
    REDIS_LIST = "productsList"
    JWT_SECRET_KEY = "JWTSecretDevKey"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=3600)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
