from datetime import datetime
import pathlib


from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from database.config import session
from models.companies import Companies
from models.employers import Employers
from models.periods import Period
from models.time import Time

from utils.pdfkit.pdfhandled import create_pdf


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
        employer_time_query = (
            session.query(Time)
            .filter(Time.employer_id == employer_id)
            .filter(Time.id == time_id)
            .one_or_none()
        )

        employers = (
            session.query(Employers)
            .filter(Employers.id == employer_id, Employers.company_id == company_id)
            .one_or_none()
        )

        company = session.query(Companies).filter(Companies.id == company_id).first()

        if not employer_time_query or not employers or not company:
            return {"ok": False, "msg": "time, employer, or company not found", "result": None}

        time = vars(employer_time_query)

        template_html = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Voucher de Pago</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #fff;
                    border: 1px solid #ccc;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }
                .header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                }
                .employer-info, .employee-info {
                    margin-bottom: 10px;
                }
                .period {
                    text-align: right;
                    margin-bottom: 20px;
                }
                .table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }
                .table th, .table td {
                    border: 1px solid #ccc;
                    padding: 8px;
                    text-align: left;
                }
                .table th {
                    background-color: #f2f2f2;
                }
                .totals {
                    margin-top: 20px;
                }
                .signature {
                    margin-top: 40px;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="employer-info">
                        <p><strong>Empleador:</strong> {{ company }}</p>
                    </div>
                    <div class="period">
                        <p><strong>Periodo de Pago:</strong> {{ start_date }} - {{ end_date }}</p>
                        <p><strong>Tipo de Pago:</strong> Semanal</p>
                    </div>
                </div>
                <div class="employee-info">
                    <p><strong>Empleado:</strong> {{ first_name }} {{ last_name }}</p>
                </div>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Concepto</th>
                            <th>Monto</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Salario Regular</td>
                            <td>${{ regular_pay }}</td>
                        </tr>
                        <tr>
                            <td>Horas Extra</td>
                            <td>${{ overtime_pay }}</td>
                        </tr>
                        <tr>
                            <td>Enfermedad</td>
                            <td>${{ sick_pay }}</td>
                        </tr>
                        <tr>
                            <td>Medicare</td>
                            <td>${{ medicare }}</td>
                        </tr>
                        <tr>
                            <td>Vacaciones</td>
                            <td>${{ vacation_pay }}</td>
                        </tr>
                        <tr>
                            <td>Seguro Social</td>
                            <td>${{ secure_social }}</td>
                        </tr>
                        <tr>
                            <td>Incapacidad</td>
                            <td>${{ inability }}</td>
                        </tr>
                    </tbody>
                </table>
                <div class="totals">
                    <p><strong>Total Ingresos:</strong> ${{ total_ingresos }}</p>
                    <p><strong>Total Egresos:</strong> ${{ total_egresos }}</p>
                    <hr>
                    <p><strong>Total a Pagar:</strong> ${{ total_a_pagar }}</p>
                </div>
                <div class="signature">
                    <p>Firma del Empleado: _________________________</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Datos para la plantilla
        info = {
            "first_name": employers.first_name,
            "last_name": employers.last_name,
            "social_security_number": employers.social_security_number,
            "periodo": "1",
            "start_date": "2",
            "end_date": "2",
            "company": company.name,
            "regular_pay": str("{0:.2f}".format(time["regular_pay"])),
            "overtime_pay": str("{0:.2f}".format(time["overtime_pay"])),
            "meal_time_pay": str("{0:.2f}".format(time["meal_time_pay"])),
            "sick_pay": str("{0:.2f}".format(time["sick_pay"])),
            "vacation_pay": str("{0:.2f}".format(time["vacation_pay"])),
            "secure_social": str("{0:.2f}".format(time["secure_social"])),
            "medicare": str("{0:.2f}".format(time["medicare"])),
            "inability": str("{0:.2f}".format(time["inability"])),
            "total_ingresos": str("{0:.2f}".format(
                time["regular_pay"] + time["overtime_pay"] + time["meal_time_pay"] + time["vacation_pay"])),
            "total_egresos": str("{0:.2f}".format(time["sick_pay"] + time["secure_social"] + time["medicare"] + time["inability"])),
            "total_a_pagar": str("{0:.2f}".format(
                (time["regular_pay"] + time["overtime_pay"] + time["meal_time_pay"] + time["vacation_pay"]) - (
                            time["sick_pay"] + time["secure_social"] + time["medicare"] + time["inability"])))
        }

        template = Template(template_html)
        rendered_html = template.render(info)

        # Generar el PDF usando WeasyPrint
        pdf_file = "voucher_pago.pdf"
        HTML(string=rendered_html).write_pdf(pdf_file)

        return FileResponse(
            pdf_file,
            media_type="application/pdf",
            filename=f"Talonario de Pagos de {employers.first_name} {employers.last_name}.pdf"
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()