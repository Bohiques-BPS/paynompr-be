import bcrypt
from datetime import datetime

from sqlalchemy.orm import aliased

from fastapi import APIRouter
from database.config import session
from schemas.companies import CompaniesSchema, CompaniesWithEmployersSchema
from sqlalchemy.orm import Session

from models.companies import Companies
from models.employers import Employers
from models.taxes import Taxes
from sqlalchemy.orm import joinedload


from models.time import Time
from models.payments import Payments

from routers.auth import user_dependency

companies_router = APIRouter()

def create_company_controller(companie_data, user): 
    companie_query = Companies(
        name=companie_data.name,
        commercial_register=companie_data.commercial_register,
        jurisdiction=companie_data.jurisdiction,
        accountant_id=companie_data.accountant_id,
        email=companie_data.email,
        employed_contribution=companie_data.employed_contribution,
        contact=companie_data.contact,
        choferil_number=companie_data.choferil_number,

        contact_number=companie_data.contact_number,
        website=companie_data.website,
        number_patronal=companie_data.number_patronal,
        vacation_hours = companie_data.vacation_hours,
        vacation_date = companie_data.vacation_date,
        sicks_hours = companie_data.sicks_hours,
        sicks_date = companie_data.sicks_date,
        coml=companie_data.coml,
        postal_address=companie_data.postal_address,
        zipcode_postal_address=companie_data.zipcode_postal_address,
        country_postal_address=companie_data.country_postal_address,
        state_postal_addess=companie_data.state_postal_addess,
        physical_address=companie_data.physical_address,
        zipcode_physical_address=companie_data.zipcode_physical_address,
        country_physical_address=companie_data.country_physical_address,
        state_physical_address=companie_data.state_physical_address,
        phone_number=companie_data.phone_number,
        fax_number=companie_data.fax_number,
        industrial_code=companie_data.industrial_code,
        payer=companie_data.payer,
        desem=companie_data.desem,
        disabled_percent=companie_data.disabled_percent,
        unemployment_percentage=companie_data.unemployment_percentage,
        code_id=user["code"],
        polize_number=companie_data.polize_number,
        driver_code=companie_data.driver_code,
        driver_rate=companie_data.driver_rate,
    )

    session.add(companie_query)

    session.commit()

    session.refresh(companie_query)
    return {"ok": True, "msg": "", "result": companie_query}

def get_all_companies_controller(user):
    companies_query = (
        session.query(Companies)
        .options(joinedload(Companies.employers))
        .filter(Companies.code_id == user["code"])
        .all()
    )

    # Filtrar manualmente los empleados con is_deleted false para cada compañía
    for company in companies_query:
        company.employers = [
            employer for employer in company.employers if not employer.is_deleted
        ]

    return companies_query

def get_all_company_and_employer_controller(user, company_id, employers_id):
    companies_query = (
        session.query(Employers, Companies)
        .join(Companies, onclause=Companies.id == company_id)
        .filter(Companies.code_id == user["code"], Employers.id == employers_id)
        .first()
    )
    employers_query = session.query(Employers).filter(Employers.company_id == company_id).all()
    employer, company = companies_query  # Desempaquetar la tupla
    simple_query = (
        session.query(Time)
        .outerjoin(Payments)
        .filter(Time.employer_id == employers_id)
        .all()
    )
    for time_obj in simple_query:
        print(
            time_obj.payment
        )  # Acceder a la relación payment definida en el modelo Time
    taxes_query = (
        session.query(Taxes)
        .filter(Taxes.company_id == company_id, Taxes.is_deleted == False)
        .all()
    )

    return {
        "ok": True,
        "msg": "",
        "result": {
            "company": company,
            "employer": employer,
            "employers": employers_query,
            "time": simple_query,
            "taxes": taxes_query,
        },
    }

def get_talonario_controller(user, company_id, employers_id, period_id):
    companies_query = (
        session.query(Employers, Companies)
        .join(Companies, onclause=Companies.id == company_id)
        .filter(Employers.id == employers_id)
        .first()
    )
    employer, company = companies_query  # Desempaquetar la tupla
    time_query = (
        session.query(Time)
        .filter(Time.employer_id == employers_id, Time.id == period_id)
        .first()
    )
    taxes_query = session.query(Payments).filter(Payments.time_id == period_id).all()

    return {
        "ok": True,
        "msg": "",
        "result": {
            "company": company,
            "employer": employer,
            "time": time_query,
            "taxes": taxes_query,
        },
    }

def get_company_controller(user, companies_id):
    companies_query = (
        session.query(Companies)
        .filter(Companies.code_id == user["code"], Companies.id == companies_id)
        .one_or_none()
    )

    return {
        "ok": True,
        "msg": "Companies were successfully retrieved",
        "result": companies_query,
    }

def get_companies_by_id_controller(companies_id):
    company_query = session.query(Companies).filter_by(id=companies_id).first()

    if not company_query:
        return {"ok": False, "msg": "Companies not found", "result": None}

    return {
        "ok": True,
        "msg": "user was successfully retrieved",
        "result": company_query,
    }


def update_company_controller(companies_id, company_data):
    company_query = session.query(Companies).filter_by(id=companies_id).one_or_none()

    if not company_query:
        return {"ok": False, "msg": "Companies not found"}
    company_query.name = company_data.name
    company_query.commercial_register = company_data.commercial_register
    company_query.jurisdiction = company_data.jurisdiction
    company_query.accountant_id = company_data.accountant_id
    company_query.email = company_data.email
    company_query.choferil_number = company_data.choferil_number
    company_query.contact = company_data.contact
    company_query.contact_number = company_data.contact_number
    company_query.website = company_data.website
    company_query.employed_contribution = company_data.employed_contribution
    company_query.postal_address = company_data.postal_address
    company_query.zipcode_postal_address = company_data.zipcode_postal_address
    company_query.country_postal_address = company_data.country_postal_address
    company_query.state_postal_addess = company_data.state_postal_addess
    company_query.number_patronal = company_data.number_patronal
    company_query.coml = company_data.coml
    company_query.vacation_hours = company_data.vacation_hours,
    company_query.vacation_date = company_data.vacation_date,
    company_query.sicks_hours = company_data.sicks_hours,
    company_query.sicks_date = company_data.sicks_date,
    company_query.physical_address = company_data.physical_address
    company_query.zipcode_physical_address = company_data.zipcode_physical_address
    company_query.country_physical_address = company_data.country_physical_address
    company_query.state_physical_address = company_data.state_physical_address
    company_query.phone_number = company_data.phone_number
    company_query.fax_number = company_data.fax_number
    company_query.industrial_code = company_data.industrial_code
    company_query.payer = company_data.payer
    company_query.desem = company_data.desem
    company_query.disabled_percent = company_data.disabled_percent
    company_query.unemployment_percentage = company_data.unemployment_percentage

    company_query.polize_number = company_data.polize_number
    company_query.driver_code = company_data.driver_code
    company_query.driver_rate = company_data.driver_rate

    session.add(company_query)
    session.commit()
    session.refresh(company_query)

    return {
        "ok": True,
        "msg": "Companies was successfully updated",
        "result": company_query,
    }



def disable_company_controller(id):
    companie_query = session.query(Companies).filter(Companies.id == id).first()

    companie_query.is_deleted = not companie_query.is_deleted
    companie_query.deleted_at = datetime.utcnow()
    session.add(companie_query)
    session.commit()
    session.refresh(companie_query)
    return {"ok": True, "msg": "", "result": companie_query}



def delete_company_controller(id):
    # Verificar si la compañía tiene empleados asociados
    employee_count = session.query(Employers).filter(Employers.company_id == id).count()

    if employee_count > 0:
        return {
            "ok": False,
            "msg": "La compañía tiene empleados y no puede ser eliminada.",
            "result": None,
        }
    # Si no hay empleados, proceder con la eliminación
    company_query = session.query(Companies).filter(Companies.id == id).first()
    if company_query:
        session.delete(company_query)
        session.commit()
        return {
            "ok": True,
            "msg": "Compañía eliminada con éxito.",
            "result": company_query,
        }
    else:
        return {"ok": False, "msg": "Compañía no encontrada.", "result": None}
