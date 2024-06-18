import bcrypt
from fastapi import APIRouter
from fastapi import APIRouter, Depends






from starlette.responses import FileResponse
from fastapi import  Response

from database.config import session
from routers.auth import user_dependency

from models.time_outemployer import TimeOutEmployer
from models.outemployers import OutEmployers
from models.companies import Companies





from schemas.time_outemployer import OutTimeIDShema, OutTimeShema, OutTimeIDShema2
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
outtime_router = APIRouter()



@outtime_router.post("/{employer_id}")
async def create_time(time_data: OutTimeShema, employer_id : int):    

    time_query = TimeOutEmployer(        
        regular_hours = time_data.regular_hours,
        regular_min = time_data.regular_min,
        regular_pay = time_data.regular_pay,
        detained = time_data.detained,
        employer_id = employer_id
    )
    session.add(time_query)
    session.commit()
    session.refresh(time_query) 
      
    return {"ok": True, "msg": "Time was successfully created", "result": time_query}

@outtime_router.get("/{employer_id}")
async def get_time_by_employer_id(employer_id: int):
    time_query = session.query(TimeOutEmployer).filter(TimeOutEmployer.employer_id == employer_id).all()

    return {
        "ok": True,
        "msg": "Employers were successfully retrieved",
        "result": time_query,
    }


@outtime_router.delete("/{time_id}")
async def delete_employer(time_id: int, user: user_dependency):
    
    # Verificar si la compañía tiene time asociados
    time_query = session.query(TimeOutEmployer).filter(TimeOutEmployer.id == time_id).first()

    
    if time_query:
        session.delete(time_query)
        session.commit()
        return {"ok": True, "msg": "Horas eliminadas con éxito.", "result": time_query}
    else:
        return {"ok": False, "msg": "Empleado no encontrada.", "result": None}
 

@outtime_router.put("/{time_id}")
async def update_time(time_id: int, time: OutTimeIDShema2):
    time_query = session.query(TimeOutEmployer).filter_by(id=time_id).first()
    if  not time_query:
        return {"ok": False, "msg": "Time was error updated", "result": time_query}
        
    time_query.regular_hours = time.regular_hours
    time_query.regular_min = time.regular_min
    time_query.detained = time.detained
   
   

    time_query.regular_pay = time.regular_pay
    
    

    session.add(time_query)
    session.commit()
    session.refresh(time_query)

          
           
    
    return {"ok": True, "msg": "Time was successfully updated", "result": time_query}


