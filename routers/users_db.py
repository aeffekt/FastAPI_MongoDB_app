from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemes.user import user_schema, users_schema
from db.client import db_client
from typing import List
from bson import ObjectId


router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.get("/", response_model=List[User])
async def users():
    users_in_db = db_client.local.users.find()    
    users_list = users_schema(users_in_db)
    return users_list


@router.post("/", status_code=201)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ese email ya se encuentra registrado")
    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))

    return User(**new_user)


@router.put("/", status_code=200)
async def user(user: User):
    user_dict = dict(user)
    del user_dict["id"]
    try:
        db_client.local.users.find_one_and_replace(
            {"_id":ObjectId(user.id)}, user_dict)
    except:
        raise HTTPException(404, detail="Usuario no encontrado")

    return search_user("_id", ObjectId(user.id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_client.local.users.find_one_and_delete({"_id":ObjectId(id)})
    if not found:        
        raise HTTPException(404, detail="Usuario no encontrado")

   

def search_user(field: str, key):
    try:
        user = user_schema(db_client.local.users.find_one({field: key}))
        print(user)
        return User(**user)
    except:
        return {"Error": "Not found"}
    