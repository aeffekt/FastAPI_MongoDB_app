from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["users"])

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name="Agustin", surname="Turko", url="www.arnaiz.com.ar", age=43),
            User(id=2, name="Marcos", surname="Tano", url="www.arnaiz.com.ar", age=23),
            User(id=3, name="Gabriel", surname="Gab", url="www.arnaiz.com.ar", age=48)]


@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)


@router.post("/user/", status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail="El usuario ya existe")
    else:
        users_list.routerend(user)        


@router.put("/user/", status_code=200)
async def user(user: User):
    for i, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[i] = user            
            return
    raise HTTPException(404, detail="Usuario no encontrado")



@router.delete("/user/{id}", status_code=200)
async def user(id: int):
    for i, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[i]
            return f"Usuario {saved_user.name} eliminado con éxito"
    raise HTTPException(404, detail="Usuario no encontrado")


@router.get("/users/")
async def users():    
    return users_list


def search_user(id: int):    
    user = list(filter(lambda user: user.id == id, users_list))        
    if user:
        return users
    return "No encontrado"
    