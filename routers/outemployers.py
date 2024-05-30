import bcrypt
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from datetime import  datetime

from database.config import session
from routers.auth import user_dependency

from models.outemployers import OutEmployers
from models.companies import Companies
from models.time import Time


from schemas.outemployers import OutEmployersSchema
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
outemployers_router = APIRouter()


@outemployers_router.post("/{company_id}")
async def create_employer(employer_data: OutEmployersSchema, company_id : int):    

    outemployer_query = OutEmployers(        
        last_name = employer_data.last_name,
        mother_last_name = employer_data.mother_last_name,
        first_name = employer_data.first_name,
        middle_name = employer_data.middle_name,
        company_id =  company_id,
        account_number = employer_data.account_number,
        email = employer_data.email,
        address = employer_data.address,
        address_state = employer_data.address_state,
        address_country = employer_data.address_country,
        address_number = employer_data.address_number,
        phone_number = employer_data.phone_number,
        smartphone_number = employer_data.smartphone_number,
        
        is_deleted = False,
        
        
        
        gender = employer_data.gender,
        birthday = employer_data.birthday,
        
    )   
    session.add(outemployer_query)
    session.commit()
    session.refresh(outemployer_query)   
    return {"ok": True, "msg": "user was successfully created", "result": outemployer_query}



@outemployers_router.get("/{company_id}")
async def get_all_outemployers_by_company_id(company_id: int,user: user_dependency):
    outemployer_query = session.query(OutEmployers).join(Companies).filter(OutEmployers.company_id == company_id, Companies.id == OutEmployers.company_id,Companies.code_id == user["code"]).all()

    return {
        "ok": True,
        "msg": "OutEmployers were successfully retrieved",
        "result": outemployer_query,
    }




@outemployers_router.get("/{company_id}/{outemployers_id}")
async def get_employer_by_id(outemployers_id: int,company_id: int,user: user_dependency):
    outemployer_query = session.query(OutEmployers).join(Companies).filter(OutEmployers.id == outemployers_id,OutEmployers.company_id == company_id, Companies.id == OutEmployers.company_id,Companies.code_id == user["code"]).first()

    if not outemployer_query:
        return {"ok": False, "msg": "user not found", "result": None}

    return {"ok": True, "msg": "Employer was successfully retrieved", "result": outemployer_query}


@outemployers_router.put("/{outemployers_id}")
async def update_employer(outemployers_id: int, employer: OutEmployersSchema, user: user_dependency):
    outemployer_query = session.query(OutEmployers).filter_by(id=outemployers_id).first()

    
    outemployer_query.last_name = employer.last_name
    outemployer_query.mother_last_name = employer.mother_last_name
    outemployer_query.first_name = employer.first_name
    outemployer_query.middle_name = employer.middle_name    
    outemployer_query.address = employer.address    
    outemployer_query.address_state = employer.address_state
    outemployer_query.address_country = employer.address_country
    outemployer_query.address_number = employer.address_number
    outemployer_query.phone_number = employer.phone_number
    outemployer_query.smartphone_number = employer.smartphone_number   
    outemployer_query.gender = employer.gender
    outemployer_query.birthday = employer.birthday   

    session.add(outemployer_query)
    session.commit()
    session.refresh(outemployer_query)

    return {"ok": True, "msg": "user was successfully updated", "result": outemployer_query}


@outemployers_router.delete("/{outemployers_id}")
async def outemployers(outemployers_id: int, user: user_dependency):
    outemployer_query = session.query(OutEmployers).join(Companies).filter(OutEmployers.id == outemployers_id, Companies.id == OutEmployers.company_id,Companies.code_id == user["code"]).first()
   
    
    
    outemployer_query.is_deleted = not outemployer_query.is_deleted    
    outemployer_query.deleted_at = datetime.utcnow()
    session.add(outemployer_query)   
    session.commit()  
    session.refresh(outemployer_query)   
    return {"ok": True, "msg": "Employer was change status", "result": outemployer_query}


