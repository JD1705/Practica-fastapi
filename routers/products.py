from fastapi import APIRouter,HTTPException
from pydantic import BaseModel

class Product(BaseModel):
    name:str
    id:int
    price:float

router = APIRouter(prefix='/products',tags=['products'])

products_list = [Product(name='Cafetera',id=0,price=12.99),
                Product(name='Helado',id=1,price=3.99),
                Product(name='Microondas',id=2,price=15.50),
                Product(name='Pan',id=3,price=2.00),
                Product(name='Hoodie',id=4,price=10.20),]

@router.get('/')
async def products_db():
    return products_list

@router.get('/{id}')
async def products_id(id:int):
    for product in products_list:
        if product.id == id:
            return product
        
    raise HTTPException(status_code=404,detail='Product Not Found')

@router.post('/product/')
async def product_create(product:Product):
    for products in products_list:
        if products.id == product.id:
            raise HTTPException(status_code=409,detail='Product Already Exist') #para lanzar las excepciones o errores de estado se usa el raise
    
    #si no existe se agrega a la DB
    products_list.append(product)
    return product
