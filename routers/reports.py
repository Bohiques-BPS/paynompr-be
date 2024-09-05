from datetime import datetime
import pathlib


from fastapi import APIRouter
from fastapi.responses import FileResponse

from controllers.reports_controller import all_counterfoil_controller, counterfoil_controller, form_940_pdf_controller, form_choferil_pdf_controller, form_sso_pdf_controller, form_unemployment_pdf_controller, form_withheld_499_pdf_controller, get_report_cfse_pdf_controller, form_w2pr_pdf_controller
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

@report_router.get("/form_w2pr_pdf/{employer_id}/{date_start}/{date_end}")
async def form_w2pr_pdf(employer_id: int, date_start: str, date_end: str):
    return form_w2pr_pdf_controller(employer_id, date_start, date_end)


@report_router.get("/form_sso_pdf")
async def form_sso_pdf():
    return form_sso_pdf_controller()

@report_router.get("/form_unemployment_pdf")
async def form_unemployment_pdf():
    return form_unemployment_pdf_controller()


@report_router.get("/form_withheld_499_pdf")
async def form_withheld_499_pdf():
    return form_withheld_499_pdf_controller()



@report_router.get("/form_choferil_pdf")
async def form_choferil_pdf():
    return form_choferil_pdf_controller()

@report_router.get("/get_report_cfse_pdf/{company_id}")
async def get_report_cfse_pdf(company_id: int):
    return get_report_cfse_pdf_controller(company_id)
