from datetime import datetime
import pathlib


from fastapi import APIRouter
from fastapi.responses import FileResponse

from database.config import session
from models.companies import Companies
from models.employers import Employers
from models.periods import Period
from models.time import Time

from utils.pdfkit.pdfhandled import create_pdf


report_router = APIRouter()


@report_router.get("/counterfoil1/{company_id}/{period_Id}")
async def all_counterfoil(company_id: int, period_Id: int):
    return {
        "ok": True,
        "msg": "Employers was successfully retrieved",
        "result": {"company": company_id, "period": period_Id},
    }


@report_router.get("/counterfoil/{company_id}/{period_id}/{employer_id}")
async def counterfoil(company_id: int, employer_id: int, period_id: int):
    employer_time_query = (
        session.query(Time)
        .filter(Time.employer_id == employer_id)
        .filter(Time.period_id == period_id)
        .one_or_none()
    )

    employers = (
        session.query(Employers)
        .filter(Employers.id == employer_id, Employers.company_id == company_id)
        .one_or_none()
    )

    company = session.query(Companies).filter(Companies.id == company_id).first()

    period = session.query(Period).filter(Period.id == period_id).first()

    time = vars(employer_time_query)

    if not employer_time_query:
        return {"ok": False, "msg": "time not found", "result": None}

    dir_path = pathlib.Path().resolve()
    template_path = f"{dir_path}/utils/pdfkit/templates/counterfoil.html"
    print(f"Ruta del archivo de plantilla: {template_path}")

    # Verifica si el archivo existe
    if not pathlib.Path(template_path).is_file():
        print("El archivo de plantilla no existe en la ruta especificada.")
    else:
        print("El archivo de plantilla existe y está listo para ser utilizado.")
    
   

    info = {
        "first_name": employers.first_name,
        "last_name": employers.last_name,
        "social_security_number": employers.social_security_number,
        "periodo": period.period_number,
        "start_date": datetime.strftime(period.period_start, "%b %d, %Y"),
        "end_date": datetime.strftime(period.period_end, "%b %d, %Y"),
        "company": company.name,
        "regular_pay": str("{0:.2f}".format(time["regular_pay"])),
        "overtime_pay": str("{0:.2f}".format(time["overtime_pay"])),
        "meal_time_pay": str("{0:.2f}".format(time["meal_time_pay"])),
        "sick_pay": str("{0:.2f}".format(time["sick_pay"])),
        "vacation_pay": str("{0:.2f}".format(time["vacation_pay"])),
        "secure_social": str("{0:.2f}".format(time["secure_social"])),
        "medicare": str("{0:.2f}".format(time["medicare"])),
        "inability": str("{0:.2f}".format(time["inability"])),
        **time,
    }

    output = create_pdf(template_path, info=info, filename="counterfoil")

    return FileResponse(
        output,
        media_type="application/octet-stream",
        filename=f"Talonario de Pagos de {employers.first_name} {employers.last_name}.pdf",
    )
