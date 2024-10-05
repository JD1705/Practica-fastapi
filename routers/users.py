from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix='/users',tags=['users'])

#servidor local: http://127.0.0.1:8000

#entidad user (o clase usuario)
class User(BaseModel):
    username:str
    id: int
    name: str
    surname: str
    age: int

#lista de usuarios para simular una base de datos
users_list = [User(username='JD1705',id=1,name='jesus',surname='perdomo',age=20),
              User(username='jc',id=2,name='juan',surname='carlos',age=2),
              User(username='elenita',id=3,name='marta',surname='elena',age=21),
              User(username='JD1705',id=4,name='jesus',surname='perdomo',age=20),
              User(username='jc',id=5,name='juan',surname='carlos',age=2),
              User(username='elenita',id=6,name='marta',surname='elena',age=21),
              User(username='JD1705',id=7,name='jesus',surname='perdomo',age=20),
              User(username='jc',id=8,name='juan',surname='carlos',age=2),
              User(username='elenita',id=9,name='marta',surname='elena',age=21),
              User(username='JD1705',id=10,name='jesus',surname='perdomo',age=20),
              User(username='jc',id=11,name='juan',surname='carlos',age=2),
              User(username='elenita',id=12,name='marta',surname='elena',age=21),
              User(username='JD1705',id=13,name='jesus',surname='perdomo',age=20),
              User(username='jc',id=14,name='juan',surname='carlos',age=2),
              User(username='elenita',id=15,name='marta',surname='elena',age=21),
              User(username='JD1705',id=16,name='jesus',surname='perdomo',age=20),
              User(username='jc',id=17,name='juan',surname='carlos',age=2),
              User(username='elenita',id=18,name='marta',surname='elena',age=21)]

#lista con los usuarios de forma no optima
@router.get('/usersjson')
async def users_json():
    return [{'name':'jesus','surname':'Perdomo','age':20},
            {'name':'juan','surname':'carlos','age':2},
            {'name':'marta','surname':'elena','age':20}]

#forma optima de mostrar la lista con los usuarios
@router.get('/')
async def users_db():
    return users_list

#peticion por un path
@router.get('/user/{id}')
async def users_per_username(id:int):
    return search_users_per_id(id)

#peticion con un query
@router.get('/userquery/')
async def users(id:int):
    return search_users_per_id(id)

#agregando un usuario a la base de datos
@router.post('/user-signin/',response_model=User,status_code=201)
async def user_create(user:User):
    #comprobando si el usuario existe en la DB
    for users in users_list:
        if users.username == user.username:
            raise HTTPException(status_code=409,detail='User Already Exist') #para lanzar las excepciones o errores de estado se usa el raise
        elif users.id == user.id:
            raise HTTPException(status_code=409,detail='User Already Exist')
    
    #si no existe se agrega a la DB
    users_list.append(user)
    return user

#actualizando los datos de un usuario
@router.put('/user/')
async def user_update(user:User):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
    
    return user

#eliminando un usuario de la base de datos
@router.delete('/user/{id}')
async def users_del(id:int):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]

#funcion para buscar un usuarion segun su nombre de usuario
def search_users_per_id(id:int):
    users = filter(lambda user: user.id==id,users_list)
    try:
        return list(users)[0]
    except:
        raise HTTPException(status_code=404,detail='User Not Found')