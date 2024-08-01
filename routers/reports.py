from datetime import datetime
import pathlib


from fastapi import APIRouter
from fastapi.responses import FileResponse

from controllers.reports_controller import all_counterfoil_controller, counterfoil_controller, form_940_pdf_controller
from database.config import session
from models.companies import Companies
from models.employers import Employers
from models.periods import Period
from models.time import Time

from utils.pdfkit.pdfhandled import create_pdf


report_router = APIRouter()


@report_router.get("/counterfoil1/{company_id}/{period_Id}")
async def all_counterfoil(company_id: int, period_Id: int):
    return all_counterfoil_controller(company_id, period_Id)

@report_router.get("/counterfoil/{company_id}/{employer_id}/{time_id}")
async def counterfoil(company_id: int, employer_id: int, time_id: int):
    return counterfoil_controller(company_id, employer_id, time_id)


@report_router.get("/form_940_pdf")
async def form_940_pdf():
    return form_940_pdf_controller()