from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import secrets
import urllib.parse
import httpx
from datetime import timedelta, datetime
from jose import jwt
from src.auth.service import create_account

from src.config.config import Config

auth_route = APIRouter()

@auth_route.get("/sign_in")
def signin():
    state = secrets.token_urlsafe(16)

    params = {
        "client_id": Config.GOOGLE_CLIENT_ID,
        "redirect_uri": Config.GOOGLE_REDIRECT_URI, # must match the one we used is creating our project
        "response_type": "code", # google give a temporary code to use as ticket to get out jwt token
        "scope": "openid email profile",# to get the user information like name email and the likes 
        "state": state, # this is the random 16 bit characters generated to prevent CSRF attack
        "access_type": "offline",  # gives you a refresh token
    }
    auth_url = Config.GOOGLE_AUTH_URL+"?"+urllib.parse.urlencode(params)
    return RedirectResponse(auth_url)

@auth_route.get("/callback")
async def auth_callback(code:str, state:str):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            Config.GOOGLE_TOKEN_URL,
            data = {
                "code": code,
                "client_id": Config.GOOGLE_CLIENT_ID,
                "client_secret": Config.GOOGLE_CLIENT_SECRET,
                "redirect_uri": Config.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
                }
            )
    token_data = token_response.json()
    access_token = token_data["access_token"]

    async with httpx.AsyncClient() as client:
        user_respnse = await client.get(
            Config.GOOGLE_USERINFO_URL,
            headers = {"Authorization": f"Bearer {access_token}"}
        )
        
    user_info = user_respnse.json()
    payload = {
        "sub": user_info["sub"],
        "email": user_info["email"],
        "name": user_info.get("name"),
        "role": ["user"],
        "exp": datetime.utcnow() + timedelta(hours=24),
        }
    jwt_token = jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    print(create_account(jwt_token))

    return {"access_token":jwt_token, "token_type":"bearer"}
