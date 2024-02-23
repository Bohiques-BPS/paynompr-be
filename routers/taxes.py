import bcrypt
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from datetime import  datetime

from database.config import session
from routers.auth import user_dependency

from models.taxes import Taxes



from schemas.taxes import TaxeIDShema, TaxeShema
from passlib.context import CryptContext



taxes_router = APIRouter()


@taxes_router.post("/{company_id}")
async def create_taxe(taxe_data: TaxeShema, company_id : int):    

    taxes_query = Taxes(        
        name = taxe_data.name,
        amount = taxe_data.amount,
        company_id = company_id,     
    )     
  
    session.add(taxes_query)
    session.commit()
    session.refresh(taxes_query)   
    return {"ok": True, "msg": "Taxes was successfully created", "result": taxes_query}



@taxes_router.get("/{company_id}")
async def get_taxes_by_company(company_id: int):
    taxe_query = session.query(Taxes).filter(Taxes.company_id == company_id).all()

    return {
        "ok": True,
        "msg": "Taxe were successfully retrieved",
        "result": taxe_query,
    }
@taxes_router.get("/{company_id}/{taxe_id}")
async def get_taxes_by_company(company_id: int,taxe_id:int):
    taxe_query = session.query(Taxes).filter(Taxes.company_id == company_id,Taxes.id == taxe_id).first()

    return {
        "ok": True,
        "msg": "Taxe were successfully retrieved",
        "result": taxe_query,
    }

@taxes_router.put("/{taxe_id}")
async def update_taxe(taxe_id: int, time: TaxeIDShema):
    taxes_query = session.query(Taxes).filter(Taxes.id==taxe_id).first()
        
    taxes_query.name = time.name,
    taxes_query.amount = time.amount,   
    

    session.add(taxes_query)
    session.commit()
    session.refresh(taxes_query)

    return {"ok": True, "msg": "Taxe was successfully updated", "result": taxes_query}



