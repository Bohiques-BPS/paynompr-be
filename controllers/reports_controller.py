from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
import fitz  # PyMuPDF


from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse, Response
from jinja2 import Template
from sqlalchemy.sql import func


from database.config import session
from models.companies import Companies
from models.employers import Employers
from models.periods import Period
from models.time import Time
from models.payments import Payments
from models.queries.queryFormW2pr import queryFormW2pr


from utils.form_499 import form_withheld_499_pdf_generator
from utils.from_choferil import form_choferil_pdf_generator
from utils.pdfkit.pdfhandled import create_pdf
from weasyprint import HTML
from utils.form_940 import form_940_pdf_generator
from utils.form_491 import form_941_pdf_generator
from utils.form_493 import form_943_pdf_generator
from utils.unemployment import form_unemployment_pdf_generator
from utils.form_w2pr import form_w2pr_pdf_generate


report_router = APIRouter()


def all_counterfoil_controller(company_id, period_Id):
    try:
        return {
                "ok": True,
                "msg": "Employers was successfully retrieved",
                "result": {"company": company_id, "period": period_Id},
            }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()

def counterfoil_controller(company_id, employer_id, time_id):
    try:
        # Obtener la información de la empresa
        company = session.query(Companies).filter(Companies.id == company_id).first()
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )

        # Obtener la información del empleado
        employer = session.query(Employers).filter(Employers.id == employer_id).first()
        if not employer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employer not found"
            )

        # Función para convertir una cadena de tiempo a minutos
        def time_to_minutes(time_str):
            printf("-------------------"+time_str)
            hours, minutes = map(int, time_str.split(':'))
            return hours * 60 + minutes

        time_period_query = session.query(Period,Time).select_from(Period).join(Time, Period.id == Time.period_id and Time.employer_id == employer_id).filter(Time.id == time_id).first()

        # employer time
        time_query = session.query(Time).filter(Time.id == time_id).first()
        all_time_query = session.query(func.sum(Time.salary).label("total_salary"),func.sum(Time.others).label("total_others"),func.sum(Time.vacation_pay).label("total_vacation_pay"),func.sum(Time.holyday_pay).label("total_holyday_pay"),func.sum(Time.sick_pay).label("total_sick_pay"),func.sum(Time.meal_pay).label("total_meal_pay"),func.sum(Time.over_pay).label("total_over_pay"),func.sum(Time.regular_pay).label("total_regular_pay"),func.sum(Time.donation).label("total_donation"),func.sum(Time.tips).label("total_tips"),func.sum(Time.aflac).label("total_aflac"),func.sum(Time.inability).label("total_inability"),func.sum(Time.choferil).label("total_choferil"),func.sum(Time.social_tips).label("total_social_tips"),func.sum(Time.asume).label("total_asume"),func.sum(Time.concessions).label("total_concessions"),func.sum(Time.commissions).label("total_commissions"),func.sum(Time.bonus).label("total_bonus"),func.sum(Time.refund).label("total_refund"),func.sum(Time.medicare).label("total_medicare"),func.sum(Time.secure_social).label("total_ss"),func.sum(Time.tax_pr).label("total_tax_pr")).select_from(Period).join(Time, Period.id == Time.period_id and Time.employer_id == employer_id).filter(Period.year == 2024,Time.employer_id == employer_id,Period.period_start <= time_period_query.Period.period_start).group_by(Period.year).all()


        all_times_query = session.query(Time).select_from(Period).join(Time, Period.id == Time.period_id and Time.employer_id == employer_id).filter(Period.year == 2024,Time.employer_id == employer_id,Period.period_start <= time_period_query.Period.period_start).all()

        total_regular_time  = "00:00"
        total_regular_time_seconds = 0

        total_over_time  = "00:00"
        total_over_time_seconds = 0

        total_mealt_time  = "00:00"
        total_mealt_time_seconds = 0

        total_vacation_time  = "00:00"
        total_vacation_time_seconds = 0

        total_sick_time  = "00:00"
        total_sick_time_seconds = 0

        total_holiday_time  = "00:00"
        total_holiday_time_seconds = 0
        for time_entry in all_times_query:
            regular_time = time_entry.regular_time
            over_time = time_entry.over_time
            mealt_time = time_entry.meal_time
            vacation_time = time_entry.vacation_time
            sick_time = time_entry.sick_time
            holiday_time = time_entry.holiday_time



            try:
                # Convertir la cadena a horas y minutos
                regular_hours, regular_minutes = map(int, regular_time.split(':'))

                # Convertir a segundos
                regular_total_seconds = regular_hours * 3600 + regular_minutes * 60

                # Convertir la cadena a horas y minutos
                over_hours, over_minutes = map(int, over_time.split(':'))

                # Convertir a segundos
                over_total_seconds = over_hours * 3600 + over_minutes * 60

                # Convertir la cadena a horas y minutos
                mealt_hours, mealt_minutes = map(int, mealt_time.split(':'))

                # Convertir a segundos
                mealt_total_seconds = mealt_hours * 3600 + mealt_minutes * 60

                # Convertir la cadena a horas y minutos
                vacation_hours, vacation_minutes = map(int, vacation_time.split(':'))

                # Convertir a segundos
                vacation_total_seconds = vacation_hours * 3600 + vacation_minutes * 60

                # Convertir la cadena a horas y minutos
                sick_hours, sick_minutes = map(int, sick_time.split(':'))

                # Convertir a segundos
                sick_total_seconds = sick_hours * 3600 + sick_minutes * 60

                # Convertir la cadena a horas y minutos
                holiday_hours, holiday_minutes = map(int, holiday_time.split(':'))

                # Convertir a segundos
                holiday_total_seconds = holiday_hours * 3600 + holiday_minutes * 60

            except ValueError:
                # Manejar formatos de tiempo inválidos (opcional)
                print(f"Formato de tiempo inválido: {regular_time}")
                continue  # Saltar a la siguiente entrada

            # Sumar los segundos al total
            total_regular_time_seconds += regular_total_seconds
            total_mealt_time_seconds += mealt_total_seconds
            total_over_time_seconds += over_total_seconds
            total_sick_time_seconds += sick_total_seconds
            total_vacation_time_seconds += vacation_total_seconds
            total_holiday_time_seconds += holiday_total_seconds


            # Convertir los segundos totales a horas y minutos
            regular_hours, remaining_seconds = divmod(total_regular_time_seconds, 3600)
            regular_minutes, regular_seconds = divmod(remaining_seconds, 60)
            total_regular_time = f"{regular_hours:02d}:{regular_minutes:02d}"
            # Convertir los segundos totales a horas y minutos
            over_hours, remaining_seconds = divmod(total_over_time_seconds, 3600)
            over_minutes, over_seconds = divmod(remaining_seconds, 60)
            total_over_time = f"{over_hours:02d}:{over_minutes:02d}"
            # Convertir los segundos totales a horas y minutos
            sick_hours, remaining_seconds = divmod(total_sick_time_seconds, 3600)
            sick_minutes, sick_seconds = divmod(remaining_seconds, 60)
            total_sick_time = f"{sick_hours:02d}:{sick_minutes:02d}"
            # Convertir los segundos totales a horas y minutos
            mealt_hours, remaining_seconds = divmod(total_mealt_time_seconds, 3600)
            mealt_minutes, mealt_seconds = divmod(remaining_seconds, 60)
            total_mealt_time = f"{mealt_hours:02d}:{mealt_minutes:02d}"
            # Convertir los segundos totales a horas y minutos
            vacation_hours, remaining_seconds = divmod(total_vacation_time_seconds, 3600)
            vacation_minutes, vacation_seconds = divmod(remaining_seconds, 60)
            total_vacation_time = f"{vacation_hours:02d}:{vacation_minutes:02d}"
            # Convertir los segundos totales a horas y minutos
            holiday_hours, remaining_seconds = divmod(total_holiday_time_seconds, 3600)
            holiday_minutes, holiday_seconds = divmod(remaining_seconds, 60)
            total_holiday_time = f"{holiday_hours:02d}:{holiday_minutes:02d}"




        payment_query = session.query(Payments).filter(Payments.time_id == time_id).all()
        payment_texts = ""
        # Crear lista de textos de pagos

        for payment in payment_query:
            amount = 0;
            if (payment.amount< 0):
                amount = payment.amount * -1
            payment_texts += f" <tr><td>{payment.name}:</td><td>${amount}</td><td></td></tr>"


        if not time_query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Time not found"
            )


        # Obtener la información del pago
        payments = session.query(Payments).filter(Payments.time_id == time_id).all()

        if not payments:
            for payment in payments:
                print(f"ID: {payment.id}, Name: {payment.name}, Amount: {payment.amount}, Value: {payment.value}")



        # Obtener la información del periodo
        period = session.query(Period).filter(Period.id == time_query.period_id).first()
        if not period:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Period not found"
            )


        # calculo del overtime_pay
        def convertir_horas_decimales(hh_mm_str):
            hours, minutes = map(int, hh_mm_str.split(':'))
            return hours + minutes / 60.0

        def regular_pay(regular_amount , regular_time, salary, others, bonus):
            time_hours = convertir_horas_decimales(regular_time)
            return regular_amount * time_hours + salary + others +bonus


        def calculate_payment(payment_type, regular_amount):
            payment_hours = convertir_horas_decimales(payment_type)
            payment_pay = payment_hours * regular_amount
            return Decimal(payment_pay).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


        def calculate_year_curr(period_type, regular_pay):
            if period_type == "monthly":
                return regular_pay * 12
            elif period_type == "biweekly":
                return regular_pay * 24
            elif period_type == "weekly":
                return regular_pay * 52

        def calculate_income():
            regu_pay = regular_pay(time_query.regular_amount, time_query.regular_time,time_query.salary,time_query.others,time_query.bonus)
            overtime_pay = calculate_payment(time_query.over_time, time_query.over_amount)
            meal_time_pay= calculate_payment(time_query.meal_time, time_query.meal_amount)
            holiday_time_pay = calculate_payment(time_query.holiday_time, time_query.regular_amount)
            sick_pay = calculate_payment(time_query.sick_time, time_query.regular_amount)
            vacation_pay = calculate_payment(time_query.vacation_time, time_query.regular_amount)
            tips_pay = time_query.tips
            commission_pay = time_query.commissions
            concessions = time_query.concessions
            return float(regu_pay)+ float(overtime_pay) + float(meal_time_pay) + float(holiday_time_pay) + float(sick_pay) + float(vacation_pay) + float(tips_pay) + float(commission_pay) + float(concessions) + float(time_query.refund)

        def calculate_egress():
            secure_social = time_query.secure_social
            ss_tips = time_query.social_tips
            medicare = time_query.medicare
            inability = time_query.inability
            choferil = time_query.choferil
            tax_pr = time_query.tax_pr

            aflac = time_query.aflac

            return float(secure_social) + float(ss_tips) + float(medicare) + float(inability) + float(choferil) + float(tax_pr)  + float(aflac) + float(time_query.asume) + float(time_query.donation)

        def calculate_payments():
            amount = 0
            for payment in payments:
                if payment.type_taxe == 1 and payment.value > 0:
                    if (payment.value > 0):
                        payment.value = payment.value * -1;

                amount += payment.amount

            return float(amount)

        def calculate_total():
            income = calculate_income()
            egress = calculate_egress()
            adicional_amount = calculate_payments()
            return round(income - egress + adicional_amount, 2)

        info = {
            # EMPLOYERS INFO
            "first_name": employer.first_name,
            "salary": time_query.salary,
            "others": time_query.others,
            "total_ss":round(all_time_query[0].total_ss, 2) ,
            "total_tax_pr":round(all_time_query[0].total_tax_pr, 2) ,
            "total_medicare":round(all_time_query[0].total_medicare, 2) ,
            "total_refund":round(all_time_query[0].total_refund, 2) ,
            "total_bonus":round(all_time_query[0].total_bonus, 2) ,
            "total_commissions" : round(all_time_query[0].total_commissions, 2) ,
            "total_tips" : round(all_time_query[0].total_tips, 2) ,
            "total_choferil" : round(all_time_query[0].total_choferil, 2) ,
            "total_inability" : round(all_time_query[0].total_inability, 2) ,
            "total_others" : round(all_time_query[0].total_others, 2) ,
            "total_asume" : round(all_time_query[0].total_asume, 2) ,
            "total_aflac" : round(all_time_query[0].total_aflac, 2) ,
            "total_donation" : round(all_time_query[0].total_donation, 2) ,
            "total_concessions" : round(all_time_query[0].total_concessions, 2) ,
            "total_social_tips" : round(all_time_query[0].total_social_tips, 2) ,
            "total_regular_pay": round(all_time_query[0].total_regular_pay, 2) ,
            "total_over_pay": round(all_time_query[0].total_over_pay, 2) ,
            "total_meal_pay": round(all_time_query[0].total_meal_pay, 2) ,
            "total_holyday_pay": round(all_time_query[0].total_holyday_pay, 2) ,
            "total_sick_pay": round(all_time_query[0].total_sick_pay, 2) ,
            "total_vacation_pay": round(all_time_query[0].total_vacation_pay, 2) ,
            "total_salary" : round(all_time_query[0].total_salary, 2) ,
            "total_regular_time" : total_regular_time ,
            "total_over_time" : total_over_time ,
            "total_meal_time" : total_mealt_time ,
            "total_holiday_time" : total_holiday_time ,
            "total_sick_time" : total_sick_time ,
            "total_vacation_time" : total_vacation_time ,


            "asume" : time_query.asume,

            "bonus": time_query.bonus,
            "aflac": time_query.aflac,

            "refund": time_query.refund,
            "donation": time_query.donation,
            "last_name": employer.last_name,
            "employer_address": employer.address,
            "employer_state": employer.address_state,
            "employer_address_number": employer.address_number,
            "employer_phone": employer.phone_number,
            "social_security_number": employer.social_security_number,
            #PERIOD INFO
            "actual_date": datetime.now().strftime("%d-%m-%Y"),
            "start_date": period.period_start,
            "end_date": period.period_end,
            "period_type": period.period_type.value,
            # COMPANY INFO
            "company": company.name,
            # TIME INFO
            "regular_hours": time_query.regular_time,
            "over_hours": time_query.over_time,
            "meal_hours": time_query.meal_time,
            "holiday_hours": time_query.holiday_time,
            "sick_hours": time_query.sick_time,


            "vacation_hours": time_query.vacation_time,
            # PAY INFO
            "regular_pay": regular_pay(time_query.regular_amount, time_query.regular_time,time_query.salary,time_query.others,time_query.bonus),
            "overtime_pay": calculate_payment(time_query.over_time, time_query.over_amount),
            "meal_time_pay": calculate_payment(time_query.meal_time, time_query.meal_amount),
            "sick_pay": calculate_payment(time_query.sick_time, time_query.regular_amount),
            "vacation_pay": calculate_payment(time_query.vacation_time, time_query.regular_amount),
            "tips_pay": time_query.tips,
            "comissions": time_query.commissions,
            "income": calculate_income(),
            "concessions" : time_query.concessions,
            "payment_texts" : payment_texts,
            # YEAR INFO
            "year_curr":calculate_year_curr(period.period_type.value, regular_pay(time_query.regular_amount, time_query.regular_time,time_query.salary,time_query.others,time_query.bonus)),
            #RATE
            "regular_rate": time_query.regular_amount,
            "over_rate": time_query.over_amount,
            # DESCUENTOS INFO
            "secure_social": time_query.secure_social,
            "ss_tips": time_query.social_tips,
            "medicare": time_query.medicare,
            "inability": time_query.inability,
            "choferil": time_query.choferil,
            "egress": calculate_egress(),
            "tax_pr": time_query.tax_pr,
            # TOTAL INFO
            "total": calculate_total()
        }


        # Plantilla HTML
        template_html = """
           <!DOCTYPE html>
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>Recibo de Pago</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        font-size: 10px; /* Tamaño de fuente más pequeño */
                        margin: 0;
                        background-color: #fff;
                        color: #000;
                    }
                    .container {
                        width: 100%;

                        border: 1px solid #000;
                        padding: 12px;
                        box-sizing: border-box;
                    }
                    .header {
                        margin-bottom: 20px;
                    }
                    .header p {
                        margin:  0;
                    }
                    .flex-container {
                        display: flex;
                        justify-content: space-between;
                    }
                    table{
                        width: 100%;}
                    .section {
                        display: flex;
                        justify-content: space-between;
                        margin-bottom: 20px;
                    }
                    .column {
                        width: 33%;
                        padding: 10px;
                        box-sizing: border-box;
                    }
                    .totals {
                        text-align: right;
                    }
                    .totals p {
                        font-size: 1.2em;
                        font-weight: bold;
                    }
                    .grid-container {
                        display: grid;
                        grid-template-columns: auto auto;
                        column-gap: 20px;
                    }
                    .grid-container p {
                        margin: 5px 0;
                    }
                    .grid-container p.amount {
                        text-align: right;
                    }
                    .middle-column, .year-column {
                        width: 10%;
                        padding: 10px;
                        box-sizing: border-box;
                        margin-left: -30px;
                    }
                    .middle-column h4, .year-column h4 {
                        text-align: center;
                    }
                    .year-column p {
                        text-align: right;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">


                        <div class="flex-container">
                            <div class="column">
                          <p>NUMERO DE CHEQUE {{ company }}</p>
                        <p>Fecha: {{ actual_date }}</p>
                                <p>{{ first_name }} {{ last_name }}</p>
                                <p>{{ employer_address }}</p>
                                <p>{{ employer_state  }} {{ employer_address_number }}</p>
                            </div>
                            <div class="column">
                                <p>{{ first_name }} {{ last_name }}</p>
                                <p>NUMERO CHEQUE: {{ company }} {{ actual_date }}</p>
                                <p>MEMO: NÓMINA {{ start_date }} - {{ end_date }}</p>
                            </div>
                        </div>
                    </div>
                    <div style="width: 100%;display: flex;flex-direction: row;">
                     <div class="column">
                   <table >
                        <tr>
                            <th>WAGES</th>
                            <th>CURR</th>
                            <th>YEAR</th>
                        </tr>
                        <tr>
                            <td>REG. PAY:</td>
                            <td>${{ regular_pay }}</td>
                            <td>${{total_regular_pay}}</td>
                        </tr>
                        <tr>
                            <td>VACATIONS:</td>
                            <td>${{ vacation_pay }}</td>
                            <td>${{ total_vacation_pay }}</td>
                        </tr>
                         <tr>
                            <td>SICK PAY:</td>
                            <td>${{ sick_pay }}</td>
                            <td>${{ total_sick_pay }}</td>
                        </tr>
                         <tr>
                            <td>OVER TIME:</td>
                            <td>${{ overtime_pay }}</td>
                            <td>${{ total_over_pay }}</td>
                        </tr>
                         <tr>
                            <td>MEAL TIME:</td>
                            <td>${{ meal_time_pay }}</td>
                            <td>${{ total_meal_pay }}</td>
                        </tr>
                         <tr>
                            <td>COMMI:</td>
                            <td>${{ comissions }}</td>
                            <td>${{ total_commissions }}</td>
                        </tr>
                         <tr>
                            <td>TIPS:</td>
                            <td>${{ tips_pay }}</td>
                            <td>${{ total_tips }}</td>
                        </tr>
                        <tr>
                            <td>CONCESSIONS:</td>
                            <td>${{ concessions }}</td>
                            <td>${{ total_concessions }}</td>
                        </tr>
                         <tr>
                            <td>SALARY:</td>
                            <td>${{ salary }}</td>
                            <td>${{ total_salary }}</td>
                        </tr>
                         <tr>
                            <td>BONUS:</td>
                            <td>${{ bonus }}</td>
                            <td>${{ total_bonus }}</td>
                        </tr>
                         <tr>
                            <td>OTHER 1:</td>
                            <td>${{ others }}</td>
                            <td>${{ total_others }}</td>
                        </tr>
                    </table>
                    </div>
                    <div class="column">
                    <table >
                        <tr>
                            <th></th>
                            <th>CURR</th>
                            <th>YEAR</th>
                        </tr>
                        <tr>
                            <td>RETIRE FUND:</td>
                            <td>${{ refund }}</td>
                            <td>${{ total_refund }}</td>
                        </tr>
                        <tr>
                            <td>ASUME:</td>
                            <td>${{ asume }}</td>
                            <td>${{total_asume}}</td>
                        </tr>
                         <tr>
                            <td>DONATIVOS:</td>
                            <td>${{ donation }}</td>
                            <td>${{ total_donation }}</td>
                        </tr>

                    </table>
                    </div>
                    <div class="column">
                    <table >
                        <tr>
                            <th></th>
                            <th>CURR</th>
                            <th>YEAR</th>
                        </tr>
                        <tr>
                            <td>INC TAX:</td>
                            <td>${{ tax_pr }}</td>
                            <td>${{ total_tax_pr }}</td>
                        </tr>
                        <tr>
                            <td>SS WITHHELD:</td>
                            <td>$0.00</td>
                            <td>$0.00</td>
                        </tr>
<tr>
                            <td>SEGURO SOCIAL:</td>
                            <td>${{ secure_social }}</td>
                            <td>${{total_ss}}</td>
                        </tr>

                         <tr>
                            <td>SS TIPS:</td>
                            <td>${{ ss_tips }}</td>
                            <td>${{ total_social_tips }}</td>
                        </tr>
                         <tr>
                            <td>MEDICARE:</td>
                            <td>${{ medicare }}</td>
                            <td>${{ total_medicare }}</td>
                        </tr>
                         <tr>
                            <td>DISABILITY:</td>
                            <td>${{ inability }}</td>
                            <td>${{ total_inability }}</td>
                        </tr>
                         <tr>
                            <td>CHAUFFEUR W:</td>
                            <td>${{ choferil }}</td>
                            <td>${{ total_choferil }}</td>
                        </tr>
                         <tr>
                            <td>REG. HOURS:</td>
                            <td>{{ regular_hours }}</td>
                            <td>{{ total_regular_time }}</td>
                        </tr>
                        <tr>
                            <td>VAC HOURS:</td>
                            <td>{{ vacation_hours }}</td>
                            <td>{{ total_vacation_time }}</td>
                        </tr>
                        <tr>
                            <td>MEAL HOURS:</td>
                            <td>{{ meal_hours }}</td>
                            <td>{{ total_meal_time }}</td>
                        </tr>
                         <tr>
                            <td>SICK HOURS:</td>
                            <td>{{ sick_hours }}</td>
                            <td>{{ total_sick_time }}</td>
                        </tr>
                         <tr>
                            <td>OVER. HOURS:</td>
                            <td>{{ over_hours }}</td>
                            <td>{{ total_over_time }}</td>
                        </tr>
                        <tr>
                            <td>HOLIDAY HOURS:</td>
                            <td>{{ holiday_hours }}</td>
                            <td>{{ total_holiday_time }}</td>
                        </tr>
                         <tr>
                            <td>AFLAC:</td>
                            <td>${{ aflac }}</td>
                            <td>${{ total_aflac }}</td>
                        </tr>
                         {{payment_texts}}
                    </table>
                   </div>
</div>
                    <div class="totals">
                        <p>Total: ${{ total }}</p>
                    </div>

                    <div class="footer">
                        <p>VAC ACUM: ENF ACUM:</p>
                    </div>
                </div>
            </body>
            </html>



        """

        template = Template(template_html)
        rendered_html = template.render(info)

        # Generar el PDF usando WeasyPrint
        pdf_file = "voucher_pago.pdf"
        HTML(string=rendered_html).write_pdf(pdf_file)

        return FileResponse(
            pdf_file,
            media_type="application/pdf",
            filename="Talonario_de_Pagos.pdf"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()


def form_w2pr_pdf_controller(company_id, employer_id, year):
    try:
        employers = []
        pdf_files = []
        if company_id is not None:
            employers = session.query(Employers.id).filter(Employers.company_id == company_id).all()
        else:
            employers = session.query(Employers.id).filter(Employers.id == employer_id).all()

        for (index, employer) in enumerate(employers, start=1):
            info = queryFormW2pr(employer.id, year)
            if info is None:
                return Response(status_code=status.HTTP_404_NOT_FOUND, content="No data found")

            template = Template(form_w2pr_pdf_generate())
            rendered_html = template.render(info)

            pdf_file = f"./output_files/form_w2pr{index}.pdf"
            HTML(string=rendered_html).write_pdf(pdf_file)
            pdf_files.append(pdf_file)


        doc3 = fitz.open()
        for file in pdf_files:
            doc3.insert_file(file)

        pdf_file = "./output_files/form_w2pr_combined.pdf"
        doc3.save(pdf_file)

        return FileResponse(
            pdf_file,
            media_type="application/pdf",
            filename="Formulario_W2PR.pdf"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()


def form_940_pdf_controller(company_id, year):
    try:
        pdf = form_940_pdf_generator(company_id, year)
        if pdf is None:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="No data found")

        if pdf:
            return FileResponse(
                pdf,
                media_type="application/pdf",
                filename="form_940.pdf"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()


def form_941_pdf_controller(company_id, year, period):
    try:
        pdf = form_941_pdf_generator(company_id, year, period)
        if pdf is None:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="No data found")

        if pdf:
            return FileResponse(
                pdf,
                media_type="application/pdf",
                filename="form_940.pdf"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()

def form_943_pdf_controller(company_id, year, period):
    try:
        pdf = form_943_pdf_generator(company_id, year, period)
        if pdf is None:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="No data found")

        if pdf:
            return FileResponse(
                pdf,
                media_type="application/pdf",
                filename="form_940.pdf"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()


def form_unemployment_pdf_controller(company_id, year, period):
    try:
        pdf = form_unemployment_pdf_generator(company_id, year, period)
        if pdf is None:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="No data found")

        if pdf:
            return FileResponse(
                pdf,
                media_type="application/pdf",
                filename="form_unemployment.pdf"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()



def form_choferil_pdf_controller(company_id, year, period):
    try:
        pdf = form_choferil_pdf_generator(company_id, year, period)
        if pdf:
            return FileResponse(
                pdf,
                media_type="application/pdf",
                filename="form_choferil.pdf"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()

def form_withheld_499_pdf_controller(company_id, year, period):
    try:
        pdf = form_withheld_499_pdf_generator(company_id, year, period)
        if pdf is None:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="No data found")

        # return pdf
        if pdf:
            return FileResponse(
                pdf,
                media_type="application/pdf",
                filename="form_withheld_499.pdf"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()


def get_report_cfse_pdf_controller(company_id):

    company = session.query(Companies).filter(Companies.id == company_id).first()
    employees = session.query(Employers).filter(Employers.company_id == company_id).all()

    try:
        info = {
            "employer_name": company.name,
            "commercial_register": company.commercial_register,
            "telefono": company.contact_number,
        }
        #plantilla html
        template_html = """

            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Reporte Planilla CFSE</title>
                <style>
                    @page {
                        size: A4 landscape; /* Configura la página en orientación horizontal */
                        margin: 20mm;
                    }

                    body {
                        font-family: Arial, sans-serif;
                        margin: 20px;
                    }

                    .header {
                        text-align: center;
                        margin-bottom: 40px;
                    }

                    .header h1, .header h2 {
                        margin: 0;
                    }

                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 20px;
                    }

                    table, th, td {
                        border: 1px solid black;
                    }

                    th, td {
                        padding: 8px;
                        text-align: left;
                    }

                    th {
                        background-color: #f2f2f2;
                        font-size: 10px;
                    }

                    .total-row {
                        font-weight: bold;
                    }
                </style>
            </head>
            <body>
                <div class="header">
                    <h4>{{ employer_name }}</h4>
                    <h4>Número de Registro: {{ commercial_register }}</h4>
                    <h4>Teléfono: {{ telefono }}</h4>
                </div>

                <table>
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Apellido</th>
                            <th>Categoría</th>
                            <th>Tercer Trimestre</th>
                            <th>Cuarto Trimestre</th>
                            <th>Primer Trimestre</th>
                            <th>Segundo Trimestre</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Aquí puedes iterar sobre tus datos para generar las filas de la tabla -->
                        <tr>
                            <td>Juan</td>
                            <td>Pérez</td>
                            <td>A</td>
                            <td>500</td>
                            <td>600</td>
                            <td>700</td>
                            <td>800</td>
                            <td>2600</td>
                        </tr>
                        <tr>
                            <td>María</td>
                            <td>González</td>
                            <td>B</td>
                            <td>400</td>
                            <td>500</td>
                            <td>600</td>
                            <td>700</td>
                            <td>2200</td>
                        </tr>
                        <!-- Agrega más filas según sea necesario -->
                        <!-- Fila de totales -->
                        <tr class="total-row">
                            <td colspan="3">Total</td>
                            <td>900</td> <!-- Suma del Tercer Trimestre -->
                            <td>1100</td> <!-- Suma del Cuarto Trimestre -->
                            <td>1300</td> <!-- Suma del Primer Trimestre -->
                            <td>1500</td> <!-- Suma del Segundo Trimestre -->
                            <td>4800</td> <!-- Total General -->
                        </tr>
                    </tbody>
                </table>
            </body>
            </html>


        """

        template = Template(template_html)
        rendered_html = template.render(info)

        # Generar el PDF usando WeasyPrint
        pdf_file = "pdf_cfse.pdf"
        HTML(string=rendered_html).write_pdf(pdf_file)

        return FileResponse(
            pdf_file,
            media_type="application/pdf",
            filename="pdf_cfse.pdf"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()