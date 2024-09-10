from models.companies import Companies
from models.employers import Employers
from models.time import Time
from database.config import session
from random import randint
from models.accountant import Accountant
from sqlalchemy import func


def getTotalAmount(company_id):
    return session.query(func.sum(Time.total_payment)).join(Employers).filter(Employers.company_id == company_id).scalar()


def getEmployersAmount(company_id):
    arrayTotal = session.query(func.sum(Time.total_payment).label('total'), Employers.id, Employers.first_name, Employers.last_name, Employers.social_security_number).join(Employers).filter(Employers.company_id == company_id).group_by(Employers.id).limit(30).all()
    employers = []
    for index, value in enumerate(arrayTotal):
        index += 1
        data = {
            f'585721236Row{index}': value.social_security_number,
            f'ORTIZTORRES LUISARow{index}': f'{value.first_name} {value.last_name}',
            f'40000Row{index}': str(round(value.total, 2)),
            f'NORow{index}': 'NO',
        }

        employers.append(data)

    return employers

def queryFormUnemployment (company_id):
    company = session.query(Companies).filter(Companies.id == company_id).first()

    # Address Company
    physicalAddressCompany = company.physical_address if company.physical_address is not None else ''
    statePhysicalAddressCompany = company.state_physical_address if company.state_physical_address is not None else ''
    countryPhysicalAddressCompany = company.country_physical_address if company.country_physical_address is not None else ''
    zipCodeAddressCompany = company.zipcode_physical_address if company.zipcode_physical_address is not None else ''

    # Calculate Total Amount
    totalAmount = round(getTotalAmount(company_id), 2)

    # Employers
    employers =  getEmployersAmount(company_id)


    data = {
        '4155960009': company.number_patronal if company.number_patronal is not None else '',
        'MODELO INDUSTRIES INC PO BOX344 San Juan PR 00936': company.name if company.name is not None else '',
        'Parte 11  Cambio de Dirección Física  Physical Change Address': company.physical_address if company.physical_address is not None else '',
        'Dirección  Address': f'{physicalAddressCompany}, {statePhysicalAddressCompany}',
        'Dirección  Address_2': f'{ countryPhysicalAddressCompany } { zipCodeAddressCompany }',
        'MODELO INDUSTRIES INC PO BOX344 San Juan PR 00936_2': company.name if company.name is not None else '',
        '2 Total Salarios Pagados anote en columna A y B Total Wages Paid enter in columns A and B': str(totalAmount),
    }

    for employer in employers:
        data.update(employer)

    return data