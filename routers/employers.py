import bcrypt
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from database.config import session

from models.employers import Employers


from schemas.employee import EmployersSchema
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
employers_router = APIRouter()


@employers_router.post("/{company_id}")
async def create_employer(employer_data: EmployersSchema, company_id : int):    

    employer_query = Employers(        
        last_name = employer_data.last_name,
        mother_last_name = employer_data.mother_last_name,
        first_name = employer_data.first_name,
        middle_name = employer_data.middle_name,
        company_id =  company_id,
        employee_type = employer_data.employee_type,
        social_security_number = employer_data.social_security_number,
        marital_status = employer_data.marital_status,
        address = employer_data.address,
        address_state = employer_data.address_state,
        address_country = employer_data.address_country,
        address_number = employer_data.address_number,
        phone_number = employer_data.phone_number,
        smartphone_number = employer_data.smartphone_number,
    )

    session.add(employer_query)
    session.commit()
    session.refresh(employer_query)
   
    return {"ok": True, "msg": "user was successfully created", "result": employer_query}


@employers_router.get("/{company_id}")
async def get_all_employers(company_id: int):
    employer_query = session.query(Employers).filter_by(company_id = company_id).all()

    return {
        "ok": True,
        "msg": "Employers were successfully retrieved",
        "result": employer_query,
    }


@employers_router.get("/{company_id}/{employers_id}")
async def get_employer_by_id(employers_id: int,company_id: int):
    employer_query = session.query(Employers).filter_by(id=employers_id,company_id = company_id).first()

    if not employer_query:
        return {"ok": False, "msg": "user not found", "result": None}

    return {"ok": True, "msg": "Employer was successfully retrieved", "result": employer_query}


@employers_router.put("/{employers_id}")
async def update_employer(employers_id: int, employer: EmployersSchema):
    employer_query = session.query(Employers).filter_by(id=employers_id).first()

        
    employer_query.last_name = employer.last_name,
    employer_query.mother_last_name = employer.mother_last_name,
    employer_query.first_name = employer.first_name,
    employer_query.middle_name = employer.middle_name,
    employer_query.employee_type = employer.employee_type,
    employer_query.social_security_number = employer.social_security_number,
    employer_query.marital_status = employer.marital_status,
    employer_query.address = employer.address,
    employer_query.address_state = employer.address_state,
    employer_query.address_country = employer.address_country,
    employer_query.address_number = employer.address_number,
    employer_query.phone_number = employer.phone_number,
    employer_query.smartphone_number = employer.smartphone_number,
    

    session.add(employer_query)
    session.commit()
    session.refresh(employer_query)

    return {"ok": True, "msg": "user was successfully updated", "result": employer_query}
