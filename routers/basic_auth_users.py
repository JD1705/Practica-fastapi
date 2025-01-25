from fastapi import FastAPI,Depends,HTTPException,status
from pydantic import BaseModel

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl='login')

class User(BaseModel):
    username:str
    id:int
    name:str
    surname:str
    age:int
    disabled:bool
    
class UserDB(User):
    password:str
    
users_db = {
    'JD1705':{
        'username':'JD1705',
        'id':0,
        'name':'Jesus',
        'surname':'Perdomo',
        'age':20,
        'disabled':False,
        'password':'123456'
    },
    'JD1705 2':{
        'username':'JD1705 2',
        'id':1,
        'name':'Jesus',
        'surname':'Perdomo',
        'age':20,
        'disabled':True,
        'password':'654321'
    }
}

async def current_user(token:str = Depends(oauth2)): #type: ignore
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='credenciales incorrectas',
            headers={'WWW-Authenticate':'Bearer'})
        
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='usuario inactivo')
    return user

def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])
    
def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])
    
@app.post('/login')
async def login(form:OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail='el usuario no es correcto')
        
    user = search_user_db(form.username)
    if not form.password == user.password: #type: ignore
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail='la contraseña no es correcto')
        
    return {'access_toke':user.username,'token_type':'bearer'} #type: ignore

@app.get('/user/me')
async def me(user:User = Depends(current_user)):
    return user
