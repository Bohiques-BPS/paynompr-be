from models.queries.queryUtils import getCompany, getEmployersAmount, roundedAmount, getAmountGroupEmployer
from utils.time_func import getPeriodTime
from utils.country import COUNTRY


def queryFormUnemployment (company_id, year, period):
    company = getCompany(company_id)['company']

    # Data Active
    date_period = getPeriodTime(period, year)
    date_start = date_period['start']
    month = date_start.month
    

    # Calculate total amount
    
    amount_count_1 =  len(getAmountGroupEmployer(company_id, year,month))
    amount_count_2 =  len(getAmountGroupEmployer(company_id, year,month+1))
    amount_count_3 =  len(getAmountGroupEmployer(company_id, year,month+2))

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
    postalAddressCompany = company.postal_address if company.postal_address is not None else ''
    statePostalAddressCompany = company.state_postal_addess if company.state_postal_addess is not None else ''
    countryPostalAddressCompany = COUNTRY[int(company.country_postal_address)-1] if COUNTRY[int(company.country_postal_address)-1] is not None else ''
    # Address Company
    physicalAddressCompany = company.physical_address if company.physical_address is not None else ''
    statePhysicalAddressCompany = company.state_physical_address if company.state_physical_address is not None else ''
    countryPhysicalAddressCompany = company.country_physical_address if company.country_physical_address is not None else ''
    zipCodeAddressCompany = company.zipcode_physical_address if company.zipcode_physical_address is not None else ''

    # Calculate Total
    unemployment_percentage = company.unemployment_percentage.split('%')[0] if company.unemployment_percentage is not None else 0

    # A % DE Incapacitados +  Aportación Patronal
    # B % DE Desempleo
    disabled_percent = float(company.disabled_percent.strip('%')) 
    text_value_porcentage_b = float(company.unemployment_percentage.strip('%')) 
    employed_contribution = company.employed_contribution if company.employed_contribution is not None else 0
    compensation_pay_a = roundedAmount(totalAmount * (text_value_porcentage_b / 100))
    compensation_pay_b = roundedAmount(totalAmount * ((disabled_percent+ float(company.driver_code)) / 100))
    total_special = roundedAmount((totalAmount / 100) * float(company.special_contribution.strip('%')))
    total_cheque_a = roundedAmount(total_special + compensation_pay_a)

    # Employers
    # employers =  getEmployersAmount(company_id)

    

    data = {
        'text_quater' : str(year)+"-"+str(period),
        'text_quarter_ended' : str(year)+"-"+str(period),
        'text_ein': company.number_patronal if company.number_patronal is not None else '',
        'text_ein_2': company.number_patronal if company.number_patronal is not None else '',
        'text_ein_3': company.number_patronal if company.number_patronal is not None else '',
        'text_name_company': company.name +"\n" + postalAddressCompany +", " + statePostalAddressCompany +", " + countryPostalAddressCompany if company.name is not None else '',
        'textarea_name_company_2': company.name +"\n" + postalAddressCompany +", " + statePostalAddressCompany +", " + countryPostalAddressCompany if company.name is not None else '',
        'textarea_company_name_3': company.name +"\n" + postalAddressCompany +", " + statePostalAddressCompany +", " + countryPostalAddressCompany if company.name is not None else '',
       

        'text_first_month': str(amount_count_1),
        'text_second_month': str(amount_count_2),
        'text_third_month': str(amount_count_3),
        'employees': tmpEmployees,
        'text_total_wages_a': str(totalAmount),
        'text_total_wages_b': str(totalAmount),
        'text_wages_contributions_a': str(totalAmount),
        'text_wages_contributions_b': str(totalAmount),
        'text_value_porcentage_a': str(company.unemployment_percentage),
        'text_value_porcentage_b': str(disabled_percent+ float(company.driver_code)),
        'text_value_porcentage_special': company.special_contribution,
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