from fastapi import FastAPI

from routers import products,users,jwt_auth_users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)

#recursos estaticos (imagenes,videos,documentos,etc)
app.mount(path='/statics',app=StaticFiles(directory='static'),name='static')

#servidor local: http://127.0.0.1:8000

'''
metodos en el protocolo HTTP o de la app

@app.get = leer datos
@app.post = crear o agregar datos
@app.put = actualizar datos
@app.delete = eliminar datos
'''

@app.get('/')
async def root():
    return '¡Hola FastAPI!'

@app.get('/url')
async def url_show():
    return { 'url_curso':'https://mouredev.com' }

#comando para iniciar el servidor: py -m uvicorn main:app --reload
