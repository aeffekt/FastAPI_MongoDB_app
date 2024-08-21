from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter()

# metodo de autenticacion, el cual siempre espera un token
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

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
        "password": "1234"
    },
    "Turko2": {
        "username": "Turko2",
        "name": "Agustin2",
        "email": "arnaizagustin2@gmail.com",
        "disable": True,
        "password": "1234"
    }    
}


def search_user_db(username: str):
    if username in users_db:
        return UserDb(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    

#definicion de funcion de dependencia para el current user en relacion a oauth2
async def current_user(token: str =Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo",            
        )
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Incorrect username")
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    return {
            "access_token": user.username, 
            "token_type": "bearer"
            }


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user