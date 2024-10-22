from datetime import datetime
from calendar import timegm
from models.queries.queryUtils import roundedAmount, getAmountVarios, getEmployer
from utils.time_func import getAgeEmployer


def queryFormW2pr(employer_id, year = None):
  try:
    if year is None:
      year = datetime.now().year

    # Data Active
    resultEmployer = getEmployer(employer_id)
    employer = resultEmployer['employer']
    company = resultEmployer['company']

    # Total amount for the employer
    amountVarios = getAmountVarios(employer_id, year)

    # Date of birth (format: YYYY-MM-DD)
    birthday = str(employer.birthday).split('-') if employer.birthday is not None else '1000-01-01'.split('-')
    age = getAgeEmployer(birthday)
    total_7 = 0
    total_wages = 0
    # Rounding amount to 2 decimal places
    rounded_amount_medicares = roundedAmount(amountVarios.medicares if amountVarios.medicares is not None else 0)
    rounded_amount_aflac = roundedAmount(amountVarios.aflac if amountVarios.aflac is not None else 0)
    rounded_amount_commissions = roundedAmount(amountVarios.commissions if amountVarios.commissions is not None else 0)
    rounded_amount_bonus = roundedAmount(amountVarios.bonus if amountVarios.bonus is not None else 0)
    rounded_amount_wages = roundedAmount(amountVarios.wages if amountVarios.wages is not None else 0 ) 
    rounded_amount_wages_26 = roundedAmount(amountVarios.wages if amountVarios.wages is not None else 0) if age <= 26 else 0.00
    rounded_amount_concessions = roundedAmount(amountVarios.concessions if amountVarios.concessions is not None else 0)
    rounded_amount_tips = roundedAmount(amountVarios.tips if amountVarios.tips is not None else 0)
    rounded_amount_donation = roundedAmount(amountVarios.donation if amountVarios.donation is not None else 0)
    
    total_wages= rounded_amount_wages
    if age <= 26:
      if (rounded_amount_wages> 40000):
        total_wages = rounded_amount_wages-40000 
        total_7 = 40000
      else:
        total_wages = 0
        total_7=rounded_amount_wages
    
      
    rounded_amount_11 = roundedAmount(rounded_amount_commissions +     total_wages  + rounded_amount_concessions + rounded_amount_tips) 
    rounded_amount_refunds = roundedAmount(amountVarios.refunds if amountVarios.refunds is not None else 0)
    rounded_amount_secures_social = roundedAmount(amountVarios.secure_social if amountVarios.secure_social is not None else 0)
    rounded_amount_social_tips = roundedAmount(amountVarios.social_tips if amountVarios.social_tips is not None else 0)
    rounded_amount_taxes_pr = roundedAmount(amountVarios.taxes_pr if amountVarios.taxes_pr is not None else 0)

    # Address Company
    physicalAddressCompany = company.physical_address if company.physical_address is not None else ''
    statePhysicalAddressCompany = company.state_physical_address if company.state_physical_address is not None else ''
    countryPhysicalAddressCompany = company.country_physical_address if company.country_physical_address is not None else ''

    n_control = company.w2_first_control

    data = {
      'name_first_user': employer.first_name if employer.first_name is not None else '',
      'name_last_user': employer.last_name if employer.last_name is not None else '',
      'address_user': employer.address if employer.address is not None else '',
      'date_birth_day': birthday[2],
      'date_birth_month': birthday[1],
      'date_birth_year': birthday[0],
      'name_company': company.name if company.name is not None else '',
      'address_company': f'{physicalAddressCompany}, {statePhysicalAddressCompany}, {countryPhysicalAddressCompany}',
      'phone_company': company.phone_number if company.phone_number is not None else '',
      'email_company': company.email if company.email is not None else '',
      'social_security_no': employer.social_security_number if employer.social_security_number is not None else '',
      'ein': company.number_patronal if company.number_patronal is not None else '',
      'total_medicares': rounded_amount_medicares,
      'total_commissions': rounded_amount_commissions,
      'total_wages': total_wages,
      'total_wages_26': total_7,
      'code_26': 'E' if total_7 > 0 else '',
      'total_concessions': rounded_amount_concessions,
      'total_tips': rounded_amount_tips,
      'total_donation': rounded_amount_donation,
      'total_aflac': rounded_amount_aflac,
      'total_11': total_wages,
      'total_20': total_7+ total_wages-rounded_amount_tips,
      'total_22': (rounded_amount_wages_26+rounded_amount_11 + rounded_amount_wages_26),
      'total_refunds': rounded_amount_refunds,
      'total_secures_social' : rounded_amount_secures_social+rounded_amount_social_tips,
      'total_social_tips': rounded_amount_social_tips,
      'total_taxes_pr': rounded_amount_taxes_pr,
      'total_time_worker': 0,
      'year_active': year,
      'n_control': n_control
    }

    return data
  except Exception as e:
    print(f'Error in queryFormW2pr: {str(e)}')
    return None

