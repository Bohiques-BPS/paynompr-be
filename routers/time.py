from fastapi import APIRouter


from database.config import session
from routers.auth import user_dependency

from models.time import Time
from models.employers import Employers
from models.payments import Payments


from schemas.time import TimeShema, TimeIDShema2
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
time_router = APIRouter()


@time_router.post("/{employer_id}")
async def create_time(time_data: TimeShema, employer_id: int):
    time_query = Time(
        regular_hours=time_data.regular_hours,
        regular_min=time_data.regular_min,
        over_hours=time_data.over_hours,
        over_min=time_data.over_min,
        holyday_pay=time_data.holyday_pay,
        meal_hours=time_data.meal_hours,
        meal_min=time_data.meal_min,
        holiday_min=time_data.holiday_min,
        holiday_hours=time_data.holiday_hours,
        sick_hours=time_data.sick_hours,
        sick_min=time_data.sick_min,
        concessions=time_data.concessions,
        commissions=time_data.commissions,
        choferil = time_data.choferil,
        inability=time_data.inability,
        medicare=time_data.medicare,
        secure_social=time_data.secure_social,
        social_tips=time_data.social_tips,
        tax_pr=time_data.tax_pr,
        vacations_hours=time_data.vacations_hours,
        vacations_min=time_data.vacations_min,
        employer_id=employer_id,
        tips=time_data.tips,
        sick_pay=time_data.sick_pay,
        vacation_pay=time_data.vacation_pay,
        meal_time_pay=time_data.meal_time_pay,
        overtime_pay=time_data.overtime_pay,
        regular_pay=time_data.regular_pay,
    )

    
    session.add(time_query)
    session.commit()
    session.refresh(time_query)

    employers = (
        session.query(Employers)
        .filter(Employers.id == employer_id)
        .one_or_none()
    )

    employers.sicks_hours = int(employers.sicks_hours)- int(time_data.sick_hours)
    employers.vacation_hours = int(employers.vacation_hours) - int(time_data.vacations_hours)

    session.add(employers)
    session.commit()
    session.refresh(employers)

    for item in time_data.payment:
        if item.requiered == 2:
            payment_query = Payments(
                name=item.name,
                amount=item.amount,
                value=item.value,
                time_id=time_query.id,
                requiered=item.requiered,
                type_taxe=item.type_taxe,
                type_amount=item.type_amount,
            )
            session.add(payment_query)
            session.commit()
        if item.requiered == 1 and item.is_active:
            payment_query = Payments(
                name=item.name,
                amount=item.amount,
                value=item.value,
                time_id=time_query.id,
                requiered=item.requiered,
                type_taxe=item.type_taxe,
                type_amount=item.type_amount,
            )
            session.add(payment_query)
            session.commit()

    return {"ok": True, "msg": "Time was successfully created", "result": time_query}


@time_router.get("/{employer_id}")
async def get_time_by_employer_id(employer_id: int):
    time_query = session.query(Time).filter(Time.employer_id == employer_id).all()

    return {
        "ok": True,
        "msg": "Employers were successfully retrieved",
        "result": time_query,
    }


@time_router.delete("/{time_id}")
async def delete_employer(time_id: int, user: user_dependency):
    # Verificar si la compañía tiene time asociados
    time_query = session.query(Time).filter(Time.id == time_id).first()

    if time_query:
        session.delete(time_query)
        session.commit()
        return {"ok": True, "msg": "Horas eliminadas con éxito.", "result": time_query}
    else:
        return {"ok": False, "msg": "Empleado no encontrada.", "result": None}


@time_router.put("/{time_id}")
async def update_time(time_id: int, time: TimeIDShema2):
    time_query = session.query(Time).filter_by(id=time_id).first()
    if not time_query:
        return {"ok": False, "msg": "Time was error updated", "result": time_query}
    
    employers = (
        session.query(Employers)
        .filter(Employers.id == time_query.employer_id)
        .one_or_none()
    )

    employers.sicks_hours = int(employers.sicks_hours)+ int(time_query.sick_hours)
    employers.vacation_hours = int(employers.vacation_hours) + int(time_query.vacations_hours)

    time_query.regular_hours = time.regular_hours
    time_query.regular_min = time.regular_min
    time_query.holyday_pay = time.holyday_pay
    time_query.over_hours = time.over_hours
    time_query.over_min = time.over_min
    time_query.concessions = time.concessions
    time_query.commissions = time.commissions
    time_query.meal_hours = time.meal_hours
    time_query.meal_min = time.meal_min
    time_query.holiday_hours = time.holiday_hours
    time_query.holiday_min = time.holiday_min
    time_query.choferil = time.choferil
    time_query.vacations_hours = time.vacations_hours
    time_query.vacations_min = time.vacations_min
    time_query.inability = time.inability
    time_query.medicare = time.medicare
    time_query.secure_social = time.secure_social
    time_query.social_tips = time.social_tips
    time_query.tax_pr = (time.tax_pr,)
    time_query.sick_hours = time.sick_hours
    time_query.sick_min = time.sick_min

    time_query.regular_pay = time.regular_pay
    time_query.sick_pay = time.sick_pay
    time_query.vacation_pay = time.vacation_pay
    time_query.meal_time_pay = time.meal_time_pay
    time_query.overtime_pay = time.overtime_pay
    time_query.tips = time.tips

    session.add(time_query)
    session.commit()
    session.refresh(time_query)

    

    employers.sicks_hours = int(employers.sicks_hours)- int(time.sick_hours)
    employers.vacation_hours = int(employers.vacation_hours) - int(time.vacations_hours)

    session.add(employers)
    session.commit()
    session.refresh(employers)

    for item in time.payment:
        payment_query = session.query(Payments).filter_by(id=item.id).first()
        if payment_query:
            if item.requiered == 2:
                payment_query.name = (item.name,)
                payment_query.amount = (item.amount,)
                payment_query.value = (item.value,)
                payment_query.requiered = (item.requiered,)
                payment_query.type_taxe = (item.type_taxe,)
                payment_query.type_amount = item.type_amount

            if item.requiered == 1 and item.is_active:
                payment_query.name = (item.name,)
                payment_query.amount = (item.amount,)
                payment_query.value = (item.value,)
                payment_query.requiered = (item.requiered,)
                payment_query.type_taxe = (item.type_taxe,)
                payment_query.type_amount = item.type_amount
        else:
            if item.requiered == 2:
                payment_query = Payments(
                    name=item.name,
                    amount=item.amount,
                    value=item.value,
                    time_id=time_query.id,
                    requiered=item.requiered,
                    type_taxe=item.type_taxe,
                    type_amount=item.type_amount,
                )

            if item.requiered == 1 and item.is_active:
                payment_query = Payments(
                    name=item.name,
                    amount=item.amount,
                    value=item.value,
                    time_id=time_query.id,
                    requiered=item.requiered,
                    type_taxe=item.type_taxe,
                    type_amount=item.type_amount,
                )

        session.add(payment_query)
        session.commit()
        session.refresh(payment_query)

    return {"ok": True, "msg": "Time was successfully updated", "result": time_query}
