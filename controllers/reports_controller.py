from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal


from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from jinja2 import Template

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
from utils.form_sso import form_sso_pdf_generator
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


        # employer time
        time_query = session.query(Time).filter(Time.id == time_id).first()

        payment_query = session.query(Payments).filter(Payments.time_id == time_id).all()
        payment_texts = ""
        # Crear lista de textos de pagos

        for payment in payment_query:
            payment_texts += f"<p>{payment.name}:</p><p class='amount'>{payment.amount}</p>"


        if not time_query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Time not found"
            )


        # Obtener la información del pago
        payments = session.query(Payments).filter(Payments.time_id == time_id).all()
        print("estamos aca ")
        # for payment in payments:
            # print(f"ID: {payment.id}, Name: {payment.name}, Amount: {payment.amount}, Value: {payment.value}")

        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )

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
                amount += payment.amount

            return float(amount)

        def calculate_total():
            income = calculate_income()
            egress = calculate_egress()
            adicional_amount = calculate_payments()
            return income - egress + adicional_amount

        info = {
            # EMPLOYERS INFO
            "first_name": employer.first_name,
            "salary": time_query.salary,
            "others": time_query.others,

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
                        padding: 20px;
                        background-color: #fff;
                        color: #000;
                    }
                    .container {
                        width: 100%;
                        margin: auto;
                        border: 1px solid #000;
                        padding: 20px;
                        box-sizing: border-box;
                    }
                    .header {
                        margin-bottom: 20px;
                    }
                    .header p {
                        margin: 5px 0;
                    }
                    .flex-container {
                        display: flex;
                        justify-content: space-between;
                    }
                    .section {
                        display: flex;
                        justify-content: space-between;
                        margin-bottom: 20px;
                    }
                    .column {
                        width: 20%;
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
                        <p>NUMERO DE CHEQUE {{ company }}</p>
                        <p>Fecha: {{ actual_date }}</p>
                        <p>Tipo de periodo: {{ period_type }}</p>
                        <div class="flex-container">
                            <div class="column">
                                <p>{{ regular_pay }}</p>
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

                    <div class="section">
                        <div class="column">
                            <h4>Desglose de Pago</h4>
                            <div class="grid-container">
                                <p>REG. PAY:</p><p class="amount">${{ regular_pay }}</p>
                                <p>VACATIONS:</p><p class="amount">${{ vacation_pay }}</p>
                                <p>SICK PAY:</p><p class="amount">${{ sick_pay }}</p>
                                <p>OVER TIME:</p><p class="amount">${{ overtime_pay }}</p>
                                <p>MEAL TIME:</p><p class="amount">${{ meal_time_pay }}</p>
                                <p>COMMI:</p><p class="amount">${{ comissions }}</p>

                                <p>TIPS:</p><p class="amount">${{ tips_pay }}</p>
                                <p>CONCESSIONS:</p><p class="amount">${{ concessions }}</p>

                                <p>SALARY:</p><p class="amount">${{ salary }}</p>
                                <p>BONUS:</p><p class="amount">${{ bonus }}</p>
                                <p>OTHER 1:</p><p class="amount">${{ others }}</p>


                            </div>
                        </div>
                        <div class="middle-column">
                            <h4>YEAR CURR</h4>
                            <p>${{ year_curr }}</p> <!-- Ejemplo de monto anual -->
                        </div>
                        <div class="year-column">
                            <h4>CURR YEAR</h4>
                            <div class="grid-container">

                                <p>RETIRE FUND:</p><p class="amount">${{ refund }}</p>
                                <p>ASUME:</p><p class="amount">$0.00</p>

                                <p>DONATIVOS:</p><p class="amount">${{ donation }}</p>
                                <p>REG RATE:</p><p class="amount">${{ regular_rate }}</p>
                                <p>OVER RATE:</p><p class="amount">${{ over_rate }}</p>
                            </div>
                        </div>
                        <div class="column">
                            <h4>TAXES</h4>
                            <div class="grid-container">
                                <p>INC TAX:</p><p class="amount">${{ tax_pr }}</p>
                                <p>SS WITHHELD:</p><p class="amount">$0.00</p>
                                <p>SS TIPS:</p><p class="amount">${{ ss_tips }}</p>
                                <p>MEDICARE:</p><p class="amount">${{ medicare }}</p>
                                <p>DISABILITY:</p><p class="amount">${{ inability }}</p>
                                <p>CHAUFFEUR W:</p><p class="amount">${{ choferil }}</p>
                                <p>REG. HOURS:</p><p class="amount">{{ regular_hours }}</p>
                                <p>VAC HOURS:</p><p class="amount">{{ vacation_hours }}</p>
                                <p>SICK HOURS:</p><p class="amount">{{ sick_hours }}</p>
                                <p>OVER. HOURS:</p><p class="amount">{{ over_hours }}</p>
                                <p>AFLAC:</p><p class="amount">{{ aflac }}</p>

                                {{payment_texts}}
                            </div>
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

def form_w2pr_pdf_controller(employer_id, date_start, date_end):
    try:
        info = queryFormW2pr(employer_id, date_start, date_end)
        template = Template(form_w2pr_pdf_generate())
        rendered_html = template.render(info)

        pdf_file = "./output_files/form_w2pr.pdf"
        HTML(string=rendered_html).write_pdf(pdf_file)

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


def form_940_pdf_controller():
    try:
        pdf = form_940_pdf_generator()
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


def form_sso_pdf_controller():
    try:
        pdf = form_sso_pdf_generator()
        if pdf:
            return FileResponse(
                pdf,
                media_type="application/pdf",
                filename="form_sso.pdf"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()

def form_unemployment_pdf_controller():
    try:
        pdf = form_unemployment_pdf_generator()
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



def form_choferil_pdf_controller():
    try:
        pdf = form_choferil_pdf_generator()
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

def form_withheld_499_pdf_controller():
    try:
        pdf = form_withheld_499_pdf_generator()
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