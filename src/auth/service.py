from jose import jwt
from src.config.config import Config


def create_account(token:str):
    data = jwt.decode(token, Config.SECRET_KEY, Config.ALGORITHM)
    return data