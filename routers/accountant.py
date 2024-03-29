import bcrypt

from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from datetime import  datetime

from database.config import session
from models.users import Role, User , Code , UserCode
from models.accountant import Accountant

from schemas.accountant import Accountants
from passlib.context import CryptContext
from routers.auth import user_dependency

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
accountant_router = APIRouter()



@accountant_router.post("/")
async def create_accountant(accountants_data: Accountants,user: user_dependency):
    is_user = (
        session.query(User)
        .where(User.email == accountants_data.email or User.phone == accountants_data.phone)
        .one_or_none()
    )
   

    if is_user:
        # Usamos una lista para guardar los mensajes de error
        errores = []

        # Comprobamos si el email o el teléfono coinciden con el usuario existente
        if is_user.email == accountants_data.email:
            errores.append(f"email: {accountants_data.email}")

        if is_user.phone == accountants_data.phone:
            errores.append(f"phone: {accountants_data.phone}")

        # Unimos los mensajes de error con "and" si hay más de uno
        msg = " and ".join(errores)

        # Usamos una expresión ternaria para asignar el valor de ok
        ok = False if errores else True

        # Devolvemos el resultado como un diccionario
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Usuario o contraseña no son validos.")

    hashed_password = bcrypt_context.hash("123456")

    user_query = User(
        name=accountants_data.name,
        lastname=accountants_data.first_last_name,
        email=accountants_data.email,
        phone=accountants_data.phone,
        password=hashed_password,
        
        role_id=3,
    )
    session.add(user_query)
    session.commit()
    accountant_query = Accountant(
        user_id=user_query.id,
        name = user_query.name,
        code_id=user["code"],
        email=accountants_data.email,
        middle_name=accountants_data.middle_name,
        first_last_name = accountants_data.first_last_name,
        second_last_name = accountants_data.second_last_name,
        company = accountants_data.company,
        phone = accountants_data.phone,
        country = accountants_data.country,
        state = accountants_data.state,
        zip_code = accountants_data.zip_code,
        identidad_ssa = accountants_data.identidad_ssa,
        identidad_bso = accountants_data.identidad_bso,
        identidad_efile = accountants_data.identidad_efile,
        address = accountants_data.address,
        employer_insurance_number = accountants_data.employer_insurance_number    
    )
    code_query = UserCode(
        user_id=user_query.id,
        code_id=user["code"],
    )    
    session.add(accountant_query)    
    session.add(code_query)
    session.commit()
    session.refresh(user_query)
    session.refresh(accountant_query)
    session.refresh(code_query)
    return {"ok": True, "msg": "user was successfully created", "result": user_query}


@accountant_router.get("/")
async def get_all_accountants(user: user_dependency):
    accountant_query = session.query(Accountant).join(User).filter(user['code'] == Accountant.code_id, User.id == Accountant.user_id ).all()
    return {
        "ok": True,
        "msg": "Accountant were successfully retrieved",
        "result": accountant_query,
    }


@accountant_router.get("/{id}")
async def get_accountant(user: user_dependency,id: int):
    accountant_query = session.query(Accountant).join(User).filter(Accountant.id == id, User.id == Accountant.user_id ).first()
    return {
        "ok": True,
        "msg": "Accountant were successfully retrieved",
        "result": accountant_query,
    }

@accountant_router.put("/{id}")
async def update_accountant(accountants_data: Accountants,user: user_dependency,id: int):
    accountant_query = session.query(Accountant).join(User).filter(Accountant.id == id, User.id == Accountant.user_id ).first()
   
    
    accountant_query.name = accountants_data.name,
    accountant_query.code_id=user["code"],
    email=accountants_data.email,
    middle_name=accountants_data.middle_name,
    accountant_query.first_last_name = accountants_data.first_last_name,
    accountant_query.second_last_name = accountants_data.second_last_name,
    accountant_query.company = accountants_data.company,
    accountant_query.phone = accountants_data.phone,
    accountant_query.country = accountants_data.country,
    accountant_query.state = accountants_data.state,
    accountant_query.zip_code = accountants_data.zip_code,
    accountant_query.identidad_ssa = accountants_data.identidad_ssa,
    accountant_query.identidad_bso = accountants_data.identidad_bso,
    accountant_query.identidad_efile = accountants_data.identidad_efile,
    accountant_query.address = accountants_data.address,
    accountant_query.employer_insurance_number = accountants_data.employer_insurance_number    
    session.add(accountant_query)   
    session.commit()  
    session.refresh(accountant_query)   
    return {"ok": True, "msg": "user was successfully created", "result": accountant_query}

@accountant_router.delete("/{id}")
async def disable_accountant(user: user_dependency,id: int):
    accountant_query = session.query(Accountant).join(User).filter(Accountant.id == id, User.id == Accountant.user_id ).first()
   
    
    accountant_query.deleted_at = datetime.utcnow()
    accountant_query.is_deleted = not accountant_query.is_deleted    
    session.add(accountant_query)   
    session.commit()  
    session.refresh(accountant_query)   
    return {"ok": True, "msg": "user was successfully created", "result": accountant_query}