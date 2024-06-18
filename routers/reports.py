from fastapi import APIRouter

from database.config import session
from models.companies import Companies
from models.employers import Employers
from models.periods import Period
from models.time import Time


report_router = APIRouter()


@report_router.post("/counterfoil/{company_id}/{period_Id}")
async def all_counterfoil(company_id: int, period_Id: int):
    return {
        "ok": True,
        "msg": "Employers was successfully retrieved",
        "result": {"company": company_id, "period": period_Id},
    }


@report_router.post("/counterfoil/{company_id}/{period_id}/{employer_id}")
async def counterfoil(company_id: int, employer_id: int, period_id: int):
    employer_time_query = (
        session.query(
            Time,
            Companies.name,
            Employers.first_name,
            Employers.last_name,
            Period.period_number,
            Period.period_start,
            Period.period_end,
        )
        .join(Companies, Time.company_id == Companies.id)
        .join(Employers, Time.employer_id == Employers.id)
        .join(Period, Time.period_id == Period.id)
        .filter(Companies.id == company_id)
        .filter(Employers.id == employer_id)
        .filter(Period.id == period_id)
    )

    print(employer_time_query)

    if not employer_time_query:
        return {"ok": False, "msg": "time not found", "result": None}

    return {
        "ok": True,
        "msg": "Employer was successfully retrieved",
        "result": employer_time_query,
    }
