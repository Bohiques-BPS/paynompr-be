from fastapi import APIRouter, HTTPException, status


from database.config import session
from routers.auth import user_dependency

from models.time import Time
from models.employers import Employers
from models.payments import Payments


from schemas.time import TimeShema, TimeIDShema2
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
time_router = APIRouter()



def create_time_controller(time_data, employer_id):
    try:
        employers = (
            session.query(Employers)
            .filter(Employers.id == employer_id)
            .one_or_none()
        )

        if not employers:
            return {"ok": False, "msg": "Employer not found"}

        time_query = Time(
            regular_time=time_data.regular_time,
            over_time=time_data.over_time,
            meal_time=time_data.meal_time,
            regular_amount=time_data.regular_amount,
            over_amount=time_data.over_amount,
            meal_amount=time_data.meal_amount,
            holiday_time=time_data.holiday_time,
            sick_time=time_data.sick_time,
            vacation_time=time_data.vacation_time,
            commissions=time_data.commissions,
            concessions=time_data.concessions,
            choferil=time_data.choferil,
            inability=time_data.inability,
            medicare=time_data.medicare,
            secure_social=time_data.secure_social,
            social_tips=time_data.social_tips,
            tax_pr=time_data.tax_pr,
            employer_id=employer_id,
            tips=time_data.tips,
            is_deleted=False,
            memo=time_data.memo
        )

        session.add(time_query)
        session.commit()
        session.refresh(time_query)

        # Actualización de las horas de enfermedad y vacaciones del empleador
        employers.vacation_hours = int(employers.vacation_hours) - int(time_data.vacation_time.split(":")[0])

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

        return {"ok": True, "msg": "Time was successfully created", "result": time_query}
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

def delete_employer_controller(time_id, user):
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
        if not time_query:
            return {"ok": False, "msg": "Time update error", "result": time_query}
        
        employers = (
            session.query(Employers)
            .filter(Employers.id == time_query.employer_id)
            .one_or_none()
        )

        if not employers:
            return {"ok": False, "msg": "Employer not found"}

        # Sumar las horas anteriores a los empleadores antes de la actualización
        employers.sick_hours = int(employers.sick_hours) + int(time_query.sick_time.split(":")[0])
        employers.vacation_hours = int(employers.vacation_hours) + int(time_query.vacation_time.split(":")[0])

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
        time_query.commissions = time.commissions
        time_query.choferil = time.choferil
        time_query.concessions = time.concessions
        time_query.tips = time.tips
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
        employers.sick_hours = int(employers.sick_hours) - int(time.sick_time.split(":")[0])
        employers.vacation_hours = int(employers.vacation_hours) - int(time.vacation_time.split(":")[0])

        session.add(employers)
        session.commit()
        session.refresh(employers)

        for item in time.payment:
            payment_query = session.query(Payments).filter_by(id=item.id).first()
            if payment_query:
                if item.requiered == 2 or (item.requiered == 1 and item.is_active):
                    payment_query.name = item.name
                    payment_query.amount = item.amount
                    payment_query.value = item.value
                    payment_query.requiered = item.requiered
                    payment_query.type_taxe = item.type_taxe
                    payment_query.type_amount = item.type_amount
            else:
                if item.requiered == 2 or (item.requiered == 1 and item.is_active):
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
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()
