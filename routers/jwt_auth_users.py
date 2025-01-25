from fastapi import APIRouter,Depends,HTTPException,status
from pydantic import BaseModel

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = 'HS256'
ACCESS_TOKEN_DURATION = 1
SECRET = "5d3b8548fe06b7fc10b977c3b37805c8636cb1029173eaf9f9a8dd08946f3971"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl='login')

crypt = CryptContext(schemes=["bcrypt"],deprecated="auto")

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
        'password':'$2a$12$9E9HZj9.zDLJdTaXiI/aT.Je9y1l0NMSQyfZohX9.5QzAnlx2fvIG'
    },
    'JD1705 2':{
        'username':'JD1705 2',
        'id':1,
        'name':'Jesus',
        'surname':'Perdomo',
        'age':20,
        'disabled':True,
        'password':'$2a$12$BggKZDOivU6tsrh3r./3d.TFEab1x5yvIJD.gmWIxGHu4wcQlqqnK'
    }
}

async def auth_user(token:str = Depends(oauth2)):
    
    exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='credenciales incorrectas',
                headers={'WWW-Authenticate':'Bearer'})
    
    try:
        user = jwt.decode(token,SECRET,algorithms=[ALGORITHM]).get('sub')
        if user == None:
            raise exception
    except JWTError:
        raise exception
    
    return search_user(user)
        
async def current_user(user:User = Depends(auth_user)): #type: ignore
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

@router.post('/login')
async def login(form:OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail='el usuario no es correcto')
        
    user = search_user_db(form.username)
    
    if not crypt.verify(form.password,user.password): #type: ignore
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail='la contraseña no es correcto')
        
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = {'sub':user.username,'exp':expire} #type:ignore
        
    return {'access_token':jwt.encode(access_token,SECRET, algorithm=ALGORITHM),'token_type':'bearer'}


@router.get('/user/me')
async def me(user:User = Depends(current_user)):
    return user 
