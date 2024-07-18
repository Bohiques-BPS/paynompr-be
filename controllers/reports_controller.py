from datetime import datetime
import pathlib


from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from jinja2 import Template

from database.config import session
from models.companies import Companies
from models.employers import Employers
from models.periods import Period
from models.time import Time

from utils.pdfkit.pdfhandled import create_pdf
from weasyprint import HTML

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
        # Datos ficticios para probar el HTML
        info = {
            "first_name": "John",
            "last_name": "Doe",
            "social_security_number": "123-45-6789",
            "start_date": "2024-07-01",
            "end_date": "2024-07-07",
            "company": "Example Company",
            "regular_pay": "500.00",
            "overtime_pay": "100.00",
            "meal_time_pay": "50.00",
            "sick_pay": "30.00",
            "vacation_pay": "40.00",
            "secure_social": "20.00",
            "medicare": "15.00",
            "inability": "10.00",
            "total_ingresos": "690.00",
            "total_egresos": "75.00",
            "total_a_pagar": "615.00"
        }

        # Plantilla HTML
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