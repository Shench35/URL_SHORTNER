from fastapi import FastAPI
from src.app.route import app_route
app = FastAPI(
    title= "URL shortner",
    description= "Works by reducing the length of any url",
    version= "0.0.1"
)

app.include_router(app_route)

