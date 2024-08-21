from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from main import settings

'''
para usar JWT: pip install "python-jose[cryptography]"
y para encriptado: pip install "passlib[bcrypt]"
'''

# openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 30

router = APIRouter(tags=["auth"])

# metodo de autenticacion, el cual siempre espera un token
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    name: str
    email: str
    disable: bool

class UserDb(User):
    password: str

users_db = {
    "Turko": {
        "username": "Turko",
        "name": "Agustin",
        "email": "arnaizagustin@gmail.com",
        "disable": False,
        "password": "$2a$12$8mGFoS6SaLpY2bylcu7dl.8DWR5zqF0S0WK546gdVbr7GG/pgoKvy"
    },
    "Turko2": {
        "username": "Turko2",
        "name": "Agustin2",
        "email": "arnaizagustin2@gmail.com",
        "disable": True,
        "password": "$2a$12$8mGFoS6SaLpY2bylcu7dl.8DWR5zqF0S0WK546gdVbr7GG/pgoKvy"
    }    
}


def search_user_db(username: str):
    if username in users_db:
        return UserDb(**users_db[username])
    

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Incorrect username")
    
    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")    
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)    
    access_token = {"sub":user.username,
                    "exp": expire}
    jwt_token = jwt.encode(access_token,
                    SECRET_KEY, 
                    algorithm=ALGORITHM)
    return {"access_token": jwt_token, "token_type": "JWT"}


async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "JWT"})
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if username == None:
            raise exception 

    except JWTError:
        raise exception
    
    return search_user(username)


#definicion de funcion de dependencia para el current user en relacion a oauth2
async def current_user(user: User =Depends(auth_user)):    
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo",            
        )
    return user


@router.get("/users/me")
async def me(user: User = Depends(current_user)):

    return user