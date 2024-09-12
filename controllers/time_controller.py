from fastapi import APIRouter, HTTPException, status
from sqlalchemy import extract


from database.config import session
from routers.auth import user_dependency

from models.time import Time
from models.vacation_times import VacationTimes
from models.employers import Employers
from models.payments import Payments
from models.companies import Companies
from models.periods import Period
from models.accountant import Accountant
from datetime import datetime
from schemas.time import TimeShema, TimeIDShema2
from passlib.context import CryptContext
from sqlalchemy import func

from utils.time_func import minutes_to_time, time_to_minutes
from decimal import ROUND_HALF_UP, Decimal

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
time_router = APIRouter()



def create_time_controller(time_data, employer_id):
    try:
        #mounth actuality
        nounth = datetime.now().month
        year = datetime.now().year

        employers = (
            session.query(Employers)
            .filter(Employers.id == employer_id)
            .one_or_none()
        )

        if not employers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario no encontrado"
            )

        accountant = (
            session.query(Accountant)
            .filter(Accountant.id == time_data.accountant_id)
            .one_or_none()
        )
        
        if not accountant:
            if not employers:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Cuenta no encontrada"
                )        
            
        #calculamos el total_payment
        regular_time=time_data.regular_time,
        over_time=time_data.over_time,
        meal_time=time_data.meal_time,
        regular_amount=employers.regular_time,
        over_amount=employers.overtime,
        meal_amount=employers.mealtime,
        holiday_time=time_data.holiday_time,
        sick_time=time_data.sick_time,
        vacation_time=time_data.vacation_time,
        commissions=time_data.commissions,
        concessions=time_data.concessions,
        choferil=time_data.choferil,
        bonus=time_data.bonus,

        others=time_data.others,
        salary=time_data.salary,


        inability=time_data.inability,
        medicare=time_data.medicare,
        secure_social=time_data.secure_social,
        social_tips=time_data.social_tips,
        tax_pr=time_data.tax_pr,
        employer_id=employer_id,
        period_id=time_data.period_id,
        tips=time_data.tips,
        is_deleted=False,
        memo=time_data.memo

        regular_time_minutes = time_to_minutes(time_data.regular_time)
        over_time_minutes = time_to_minutes(time_data.over_time)
        meal_time_minutes = time_to_minutes(time_data.meal_time)
        holiday_time_minutes = time_to_minutes(time_data.holiday_time)
        sick_time_minutes = time_to_minutes(time_data.sick_time)
        vacation_time_minutes = time_to_minutes(time_data.vacation_time)

        # Convertir montos a números decimales si es necesario
        regular_amount = employers.regular_time
        over_amount = employers.overtime
        meal_amount = employers.mealtime

        # Calculamos el total_payment
        total_income = (
            (regular_time_minutes * regular_amount / 60) +
            (over_time_minutes * over_amount / 60) +
            (meal_time_minutes * meal_amount / 60) +
            (holiday_time_minutes * regular_amount / 60) +
            (sick_time_minutes * regular_amount / 60) +
            (vacation_time_minutes * regular_amount / 60)+
            time_data.commissions +
            time_data.concessions +
            time_data.tips)

        total_egress =(
            time_data.choferil +
            time_data.inability +
            time_data.medicare +
            time_data.secure_social +
            time_data.social_tips +
            time_data.tax_pr
        )

        total_payment = total_income - total_egress

        time_query = Time(

            regular_pay=time_data.regular_pay,
            over_pay=time_data.overtime_pay,
            meal_pay=time_data.meal_time_pay,
            sick_pay=time_data.sick_pay,
            holyday_pay=time_data.holyday_pay,  
            vacation_pay = time_data.vacation_pay,          
            
            regular_time=time_data.regular_time,
            over_time=time_data.over_time,
            meal_time=time_data.meal_time,
            regular_amount=employers.regular_time,
            over_amount=employers.overtime,
            meal_amount=employers.mealtime,
            refund=time_data.refund,
            donation=time_data.donation,
            asume=time_data.asume,
            aflac=time_data.aflac,
            accountant_id=time_data.accountant_id,

            holiday_time=time_data.holiday_time,
            sick_time=time_data.sick_time,
            vacation_time=time_data.vacation_time,
            commissions=time_data.commissions,
            concessions=time_data.concessions,
            salary=time_data.salary,

            others=time_data.others,
            bonus=time_data.bonus,

            choferil=time_data.choferil,
            inability=time_data.inability,
            medicare=time_data.medicare,
            secure_social=time_data.secure_social,
            social_tips=time_data.social_tips,
            tax_pr=time_data.tax_pr,
            employer_id=employer_id,
            period_id=time_data.period_id,
            tips=time_data.tips,
            is_deleted=False,
            memo=time_data.memo,
            total_payment = total_payment
            )

        session.add(time_query)
        session.commit()
        session.refresh(time_query)

        #actualizar horas de vaciones y de enfermedad de el empleado
        """ if time_data.vacation_time:
            current_vacation_time = time_to_minutes(employers.vacation_time)
            new_vacation_time = time_to_minutes(time_data.vacation_time)
            employers.vacation_time = minutes_to_time(current_vacation_time + new_vacation_time)

        if time_data.sick_time:
            current_sick_time = time_to_minutes(employers.sick_time)
            new_sick_time = time_to_minutes(time_data.sick_time)
            employers.sick_time = minutes_to_time(current_sick_time + new_sick_time)
        """

        session.add(employers)
        session.commit()
        session.refresh(employers)

        for item in time_data.payment:
            payment_query = Payments(
                name=item.name,
                amount=item.amount,
                value=item.value,
                time_id=time_query.id,
                is_active=item.is_active,
                required=item.required,
                type_taxe=item.type_taxe,
                type_amount=item.type_amount,
            )
            session.add(payment_query)
            session.commit()
        
        return {"ok": True, "msg": "Time was successfully created", "result": {"time": time_query} }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()

def get_time_by_employer_id_controller(employer_id):
    try:
        time_query = session.query(Time).filter(Time.employer_id == employer_id).all()

        return {
            "ok": True,
            "msg": "Employers were successfully retrieved",
            "result": time_query,
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()
def get_all_data_time_employer_controller(company_id: int, employer_id: int, time_id: int):
    try:
        company_query = session.query(Companies).filter(Companies.id == company_id).first()
    
        time_query = session.query(Time).filter(Time.id == time_id).first()
        total_amounts_by_employer = session.query(
        Employers.id,
        func.sum(Time.total_payment).label('total_amount')
        ).join(Time).filter(
        Employers.company_id == company_id
        ).group_by(Employers.id).all()

        # Convert the result to a list of dictionaries
        total_amounts_by_employer_dict = [
        {"employer_id": employer_id, "total_amount": total_amount}
        for employer_id, total_amount in total_amounts_by_employer
        ]

        if not company_query  or not time_query:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company, Employer, or Time not found"
            )

        total_amount = session.query(func.sum(Time.total_payment)).join(Employers).filter(Employers.company_id == company_id).scalar()

        return {
        "ok": True,
        "msg": "Data successfully retrieved",
        "result": {
        'time': time_query,
        'company': company_query,
        'total_amounts_by_employer': total_amounts_by_employer_dict,
        'total_amount': total_amount
        },
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()
        
def delete_time_controller(time_id, user):
    try:
        # Verificar si la compañía tiene time asociados
        time_query = session.query(Time).filter(Time.id == time_id).first()

        if time_query:
            session.delete(time_query)
            session.commit()
            return {"ok": True, "msg": "Horas eliminadas con éxito.", "result": time_query}
        else:
            return {"ok": False, "msg": "Empleado no encontrada.", "result": None}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()


def update_time_controller(time_id, time):
    try:
        time_query = session.query(Time).filter_by(id=time_id).first()
        update_vaction_time_controller(time_query.employer_id,time_query.period.period_start)
        if not time_query:
            return {"ok": False, "msg": "Time update error", "result": time_query}
        
        employers = (
            session.query(Employers)
            .filter(Employers.id == time_query.employer_id)
            .one_or_none()
        )

        if not employers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario no encontrado"
            )

        accountant = (
            session.query(Accountant)
            .filter(Accountant.id == time_query.accountant_id)
            .one_or_none()
        )
        
        if not accountant:
            if not employers:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Cuenta no encontrada"
                )        
        
        # Sumar las horas anteriores a los empleadores antes de la actualización
        #employers.sick_hours = int(employers.sick_hours) + int(time_query.sick_time.split(":")[0])
        #employers.vacation_hours = int(employers.vacation_hours) + int(time_query.vacation_time.split(":")[0])

        # Actualizar los campos del modelo Time
        time_query.regular_time = time.regular_time
        time_query.over_time = time.over_time
        time_query.meal_time = time.meal_time
        time_query.holiday_time = time.holiday_time
        time_query.sick_time = time.sick_time
        time_query.vacation_time = time.vacation_time
        time_query.regular_amount = time.regular_amount
        time_query.over_amount = time.over_amount
        time_query.meal_amount = time.meal_amount
        time_query.salary = time.salary
        time_query.refund = time.refund

        time_query.regular_pay=time.regular_pay,
        time_query.over_pay=time.overtime_pay,
        time_query.meal_pay=time.meal_time_pay,
        time_query.sick_pay=time.sick_pay,
        time_query.vacation_pay=time.vacation_pay,

        time_query.holyday_pay=time.holyday_pay, 

        time_query.donation = time.donation
        time_query.asume = time.asume
        time_query.accountant_id=time.accountant_id,


        time_query.commissions = time.commissions
        time_query.choferil = time.choferil
        time_query.concessions = time.concessions
        time_query.tips = time.tips
        time_query.aflac = time.aflac
        time_query.inability = time.inability
        time_query.medicare = time.medicare
        time_query.secure_social = time.secure_social
        time_query.social_tips = time.social_tips
        time_query.tax_pr = time.tax_pr
        time_query.memo = time.memo

        session.add(time_query)
        session.commit()
        session.refresh(time_query)

        # Restar las nuevas horas de los empleadores después de la actualización
        #employers.sick_hours = int(employers.sick_hours) - int(time.sick_time.split(":")[0])
        #employers.vacation_hours = int(employers.vacation_hours) - int(time.vacation_time.split(":")[0])

        session.add(employers)
        session.commit()
        session.refresh(employers)

        for item in time.payment:
            payment_query = session.query(Payments).filter_by(id=item.id).first()
            if payment_query:
                if item.required == 2 or (item.required == 1 and item.is_active):
                    payment_query.name = item.name
                    payment_query.amount = item.amount
                    payment_query.value = item.value
                    payment_query.required = item.required
                    payment_query.type_taxe = item.type_taxe
                    payment_query.type_amount = item.type_amount
            else:
                if item.required == 2 or (item.required == 1 and item.is_active):
                    payment_query = Payments(
                        name=item.name,
                        amount=item.amount,
                        value=item.value,
                        time_id=time_query.id,
                        required=item.required,
                        type_taxe=item.type_taxe,
                        type_amount=item.type_amount,
                    )

            session.add(payment_query)
            session.commit()
            session.refresh(payment_query)

        return {"ok": True, "msg": "Time was successfully updated", "result": time_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()



#updatear las vaciones
def update_vaction_time_controller(employer_id, date_period):

    #verificar el calculo del mes por periodo para el registro actual
    #si vacatation_time en times > 0
    #sumaro restar o empleados
    year = date_period.year
    month = date_period.month
    employer = (
                    session.query(Employers)
                    .filter(Employers.id == employer_id)
                    .one_or_none()
                )
    #times = session.query(Time).filter(Time.employer_id == employer_id).join(Period).filter(Period.id==Time.period_id,Period.year== year)
    times = session.query(Time).filter(Time.employer_id == employer_id).join(Period).filter(
            Period.id == Time.period_id,
            Period.year == year,
            extract('month', Period.period_start) == month
        ).all()
    
    if times:
        hours_worked = 0
        for time in times:
            hours_worked += time_to_minutes(time.regular_time) / 60
    
        if employer.vacation_hours_monthly <= hours_worked:
            vacation_time = session.query(VacationTimes).where(employer_id == employer_id, year == year, month == month).first()
            if not vacation_time:
                vacation_query = VacationTimes(
                    employer_id = employer_id,
                    vacation_hours = employer.vacation_hours,
                    year = year,
                    month = month

                )
                session.add(vacation_query)
                session.commit()
                session.refresh(vacation_query)
                

    
        print("work", hours_worked)
   
        
    