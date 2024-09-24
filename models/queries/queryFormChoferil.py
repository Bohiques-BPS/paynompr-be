from models.queries.queryUtils import getCompany, getEmployersAmount, roundedAmount
from utils.time_func import getPeriodTime
from datetime import datetime, date

def queryFormChoferil (company_id, year, periodo):

    company = getCompany(company_id)['company']

    date_period = getPeriodTime(periodo, year)
    dateToday = datetime.now()

    employees = getEmployersAmount(company.id, date_period)

    index = 1
    totalAmount = 0
    totalWeeks = 0
    arrayEmployees = []
    for value in employees:
        data = {
            f'text_social_employee_{index}': value.social_security_number if value.social_security_number is not None else '',
            f'text_name_{index}': f'{value.first_name} {value.last_name}',
            f'text_license_number_{index}': value.licence if value.licence is not None else '',
            f'text_total_weeks_{index}': str(value.total_weeks) if value.total_weeks is not None else '',
        }

        totalWeeks += value.total_weeks
        arrayEmployees.append(data)
        totalAmount += roundedAmount(value.total)
        index += 1

    data = {
        'text_date_end': str(date_period['end']),
        'text_total_weeks_paid': str(totalWeeks),
        'text_total_tax_due': str(totalAmount),
        'text_payment_ampunt': '0',
        'text_position': '--',
        'text_phone': company.phone_number if company.phone_number is not None else '',
        'text_date': f'{dateToday.year}-{dateToday.month}-{dateToday.day}'
    }

    for employee in arrayEmployees:
        data.update(employee)

    return data