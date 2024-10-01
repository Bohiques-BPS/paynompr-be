from models.queries.queryUtils import getCompany, getEmployersAmount, roundedAmount
from utils.time_func import getPeriodTime


def queryFormUnemployment (company_id, year, period):
    company = getCompany(company_id)['company']

    # Data Active
    date_period = getPeriodTime(period, year)

    employees = getEmployersAmount(company.id, date_period)

    arrayEmployees = []
    tmpEmployees = []
    index = 1
    totalAmount = 0
    print("-----------------employees2----------------"+str(employees))
    for value in employees:
        data = {
            f'text_social_security_{index}': value.social_security_number,
            f'text_name_employers_{index}': f'{value.first_name} {value.last_name}',
            f'text_wages_employer_{index}': str(round(value.total, 2)),
            f'text_yes_or_no_{index}': 'NO',
        }

        tmpEmployees.append(data)
        totalAmount += roundedAmount(value.total)
        index += 1
        # if len(tmpEmployees) == 24:
        #     arrayEmployees.append(tmpEmployees)
        #     tmpEmployees = []
        #     index = 1
    print("-----------------tmpEmployees----------------"+str(tmpEmployees))

    # Address Company
    physicalAddressCompany = company.physical_address if company.physical_address is not None else ''
    statePhysicalAddressCompany = company.state_physical_address if company.state_physical_address is not None else ''
    countryPhysicalAddressCompany = company.country_physical_address if company.country_physical_address is not None else ''
    zipCodeAddressCompany = company.zipcode_physical_address if company.zipcode_physical_address is not None else ''

    # Calculate Total
    unemployment_percentage = company.unemployment_percentage.split('%')[0] if company.unemployment_percentage is not None else 0
    employed_contribution = company.employed_contribution if company.employed_contribution is not None else 0
    compensation_pay_a = roundedAmount(totalAmount * (float(employed_contribution) / 100))
    compensation_pay_b = roundedAmount(totalAmount * (1 / 100))
    total_special = roundedAmount((totalAmount / 100) * float(unemployment_percentage))
    total_cheque_a = roundedAmount(total_special + compensation_pay_a)

    # Employers
    # employers =  getEmployersAmount(company_id)


    data = {
        'text_ein': company.number_patronal if company.number_patronal is not None else '',
        'text_ein_2': company.number_patronal if company.number_patronal is not None else '',
        'text_ein_3': company.number_patronal if company.number_patronal is not None else '',
        'text_name_company': company.name if company.name is not None else '',
        'textarea_name_company_2': company.name if company.name is not None else '',
        'textarea_company_name_3': company.name if company.name is not None else '',
        'text_address_company': company.physical_address if company.physical_address is not None else '',
        'text_address_company_2': f'{physicalAddressCompany}, {statePhysicalAddressCompany}',
        'text_zipcode_company': f'{ countryPhysicalAddressCompany } { zipCodeAddressCompany }',
        'employees': tmpEmployees,
        'text_total_wages_a': str(totalAmount),
        'text_total_wages_b': str(totalAmount),
        'text_wages_contributions_a': str(totalAmount),
        'text_wages_contributions_b': str(totalAmount),
        'text_value_porcentage_a': employed_contribution if employed_contribution != 0 else '',
        'text_value_porcentage_b': '1.00',
        'text_value_porcentage_special': unemployment_percentage if unemployment_percentage != 0 else '',
        'text_compensation_pay_a': str(compensation_pay_a),
        'text_compensation_pay_b': str(compensation_pay_b),
        'text_total_special': str(total_special),
        'text_total_cheque_a': str(total_cheque_a),
        'text_total_cheque_b': str(compensation_pay_b),
        'text_total_employers': str(totalAmount),
        'text_total_wages': str(len(tmpEmployees))
    }

    for employee in tmpEmployees:
        data.update(employee)


    return data