from fastapi import APIRouter, Depends
from controllers.period import create_weekly_periods, create_biweekly_periods, create_monthly_periods
from schemas.period import PeriodCreate, PeriodRead

period_routes = APIRouter()


@period_routes.post("/weekly/", response_model=list[PeriodRead])
def create_weekly_periods_route(year: int):
    return create_weekly_periods(year)

@period_routes.post("/biweekly/", response_model=list[PeriodRead])
def create_biweekly_periods_route(year: int):
    return create_biweekly_periods(year)

@period_routes.post("/monthly/", response_model=list[PeriodRead])
def create_monthly_periods_route(year: int):
    return create_monthly_periods(year)