from sqlalchemy import or_
from starlette import status

from fastapi import APIRouter, Depends, HTTPException

from database.config import session
from models.codes import Code
from schemas.codes import CodeSchema

code_router = APIRouter()


@code_router.post("/")
async def create_code(code_data: CodeSchema):
    is_code = (
        session.query(Code)
        .where(or_(Code.code == code_data.code, Code.email == code_data.email))
        .one_or_none()        
    )

    if is_code:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Correo o código ya están registrados.")

    code_query = Code(
        code = code_data.code,

        amount = code_data.amount,
        owner = code_data.owner,
        email = code_data.email,
    )  
 
    session.add(code_query)
    session.commit()
    session.refresh(code_query)

    return {"ok": True, "msg": "user was successfully created", "result": code_query}


def create_code():
    code = "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(6)
    )
    # Validar luego que no este repetido
    is_code = session.query(Code).where(Code.code == code).one_or_none()

    return code


@code_router.get("/")
async def get_all_codes():
    codes_query = session.query(Code).all()

    return {
        "ok": True,
        "msg": "users were successfully retrieved",
        "result": codes_query,
    }


@code_router.get("/{code_id}")
async def get_code_by_id(code_id: int):
    code_query = session.query(Code).filter_by(id=code_id).first()

    if not code_query:
        return {"ok": False, "msg": "user not found", "result": None}

    return {"ok": True, "msg": "Lista de codigos.", "result": code_query}
