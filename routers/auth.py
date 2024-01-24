from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database.config import Session as local
from models.users import User
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import or_


auth_router = APIRouter()

SECRET_KEY = 'DEMO'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')



class Token(BaseModel):
    access_token: str
    token_type : str

def get_db():
    db = local()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency
                                 ):
    user = authenticate_user(form_data.username,form_data.password,db)
   
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Usuario o contraseña no son validos.")
    token = create_access_token(user.email, user.id, timedelta(minutes=20))

    return {'access_token': token, "token_type": "bearer"}
   


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(or_(User.email == username, User.phone == username)).first()       
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password ):
        return False
    return user


def create_access_token(username: str, user_id: int,expires_delta : timedelta):
    encode = {'sub':username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY, algorithm=ALGORITHM)
















