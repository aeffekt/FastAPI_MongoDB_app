from fastapi import APIRouter


router = APIRouter(prefix="/products", 
                   tags=["products"],    # la documentacion agrupa con este tag la vista
                   responses={404: {"message": "No encontrado"}})


products_list = ["P1", "P2", "P3", "P4", "P5"]


@router.get("/")
async def products():
    return products_list


@router.get("/{id}")
async def products(id: int):
    return products_list[id]