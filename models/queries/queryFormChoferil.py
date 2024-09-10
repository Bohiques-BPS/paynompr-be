from models.companies import Companies
from models.employers import Employers
from models.time import Time
from database.config import session
from random import randint
from models.accountant import Accountant
from sqlalchemy import func, and_
from utils.time_func import getPeriodTime


def getTotalAmountAndWeeks(company_id, year, periodo):
    period = getPeriodTime(periodo, year)
    diferent = period['end_date'] - period['start_date']
    weeks = diferent.days // 7

    result = session.query(func.sum(Time.total_payment)).join(Employers).filter(
      and_(
        Employers.company_id == company_id,
        Time.created_at.between(period['start_date'], period['end_date'])
      )
    ).scalar()

    return {
      'total_amount': result,
      'weeks': weeks
    }


def queryFormChoferil (company_id, year, periodo):
    company = session.query(Companies).filter(Companies.id == company_id).first()

    # Address Company
    physicalAddressCompany = company.physical_address if company.physical_address is not None else ''
    statePhysicalAddressCompany = company.state_physical_address if company.state_physical_address is not None else ''
    countryPhysicalAddressCompany = company.country_physical_address if company.country_physical_address is not None else ''
    zipCodeAddressCompany = company.zipcode_physical_address if company.zipcode_physical_address is not None else ''

    # Calculate Total Amount
    totalAmountAndWeeks = getTotalAmountAndWeeks(company_id, year, periodo)

    data = {
        'txtNombrePatrono': company.name if company.name is not None else '',
        'Parte 11  Cambio de Dirección Física  Physical Change Address': company.physical_address if company.physical_address is not None else '',
        'txtNumeroCuenta': company.polize_number if company.polize_number is not None else '',
        'txtEMail': company.email if company.email is not None else '',
        'txtPhone': company.phone_number if company.phone_number is not None else '',
        'txtPostal1': physicalAddressCompany,
        'txtPostal2': statePhysicalAddressCompany,
        'txtPostal3': countryPhysicalAddressCompany,
        'txtPostal4': zipCodeAddressCompany,
        'dicTotalTaxDue': str(round(totalAmountAndWeeks['total_amount'], 2)) if totalAmountAndWeeks['total_amount'] is not None else '0.00',
        'intTotalWeek': str(totalAmountAndWeeks['weeks']),
        'intYear': str(year),
        'intQuarter': str(periodo),
    }

    return data