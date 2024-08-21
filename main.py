from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic_settings import BaseSettings, SettingsConfigDict


# uso de settings en fastapi con dotenv: pip install pydantic-settings
class Settings(BaseSettings):
    app_name: str = "MONGO API"    
    secret_key: str
    mongodb_name: str
    mongodb_pwd: str
    model_config = SettingsConfigDict(env_file=".env")    

# instancia para las settings del programa
settings = Settings()

app = FastAPI()

from routers import jwt_auth, users, products

# routers
app.include_router(users.router)
app.include_router(products.router)
app.include_router(jwt_auth.router)


# static resources
app.mount("/static", StaticFiles(directory="static"), name="static")


# HOME
@app.get("/")
async def home():
    return f"{settings.app_name}"