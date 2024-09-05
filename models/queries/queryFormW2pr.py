from models.companies import Companies
from models.employers import Employers
from models.time import Time
from database.config import session
from sqlalchemy import func, and_


def getAmountVarios(employer_id, date_start=None, date_end=None):
    result = session.query(
      func.sum(Time.total_payment).label('wages'),
      func.sum(Time.commissions).label('commissions'),
      func.sum(Time.concessions).label('concessions'),
      func.sum(Time.tips).label('tips'),
      func.sum(Time.donation).label('donation'),
      func.sum(Time.refund).label('refunds'),
      func.sum(Time.medicare).label('medicares'),
      func.sum(Time.bonus).label('bonus'),
      func.sum(Time.social_tips).label('social_tips'),
      func.sum(Time.secure_social).label('secure_social'),
      func.sum(Time.tax_pr).label('taxes_pr')
      ).filter(
        and_(
          Employers.id == employer_id,
          Time.created_at.between(date_start, date_end)
        )
      ).all()

    return result[0]

def roundedAmount(amount, decimal = 2):
    # Rounding amount to 2 decimal places
    if amount is not None:
      return round(amount, decimal)
    else:
      return 0.00

def queryFormW2pr(employer_id, date_start, date_end):
  # Initializing variables
  yearActive = date_start.split('-')[0]
  # Data Active
  employer = session.query(Employers).filter(Employers.id == employer_id).first()
  company = session.query(Companies).filter(Companies.id == employer.company_id).first()
  amountVarios = getAmountVarios(1, date_start, date_end)

  # Rounding amount to 2 decimal places
  rounded_amount_medicares = roundedAmount(amountVarios.medicares)
  rounded_amount_commissions = roundedAmount(amountVarios.commissions)
  rounded_amount_wages = roundedAmount(amountVarios.wages)
  rounded_amount_concessions = roundedAmount(amountVarios.concessions)
  rounded_amount_tips = roundedAmount(amountVarios.tips)
  rounded_amount_donation = roundedAmount(amountVarios.donation)
  rounded_amount_11 = rounded_amount_commissions + rounded_amount_wages + rounded_amount_concessions + rounded_amount_tips
  rounded_amount_refunds = roundedAmount(amountVarios.refunds) + roundedAmount(amountVarios.bonus)
  rounded_amount_secures_social = roundedAmount(amountVarios.secure_social)
  rounded_amount_social_tips = roundedAmount(amountVarios.social_tips)
  rounded_amount_taxes_pr = roundedAmount(amountVarios.taxes_pr)

  # Date of birth (format: YYYY-MM-DD)
  birthday = str(employer.birthday).split('-') if employer.birthday is not None else '0000-00-00'.split('-')

  # Address Company
  physicalAddressCompany = company.physical_address if company.physical_address is not None else ''
  statePhysicalAddressCompany = company.state_physical_address if company.state_physical_address is not None else ''
  countryPhysicalAddressCompany = company.country_physical_address if company.country_physical_address is not None else ''

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
    'social_security_no': company.number_patronal if company.number_patronal is not None else '',
    'ein': company.number_patronal if company.number_patronal is not None else '',
    'total_medicares': rounded_amount_medicares,
    'total_commissions': rounded_amount_commissions,
    'total_wages': rounded_amount_wages,
    'total_concessions': rounded_amount_concessions,
    'total_tips': rounded_amount_tips,
    'total_donation': rounded_amount_donation,
    'total_11': rounded_amount_11,
    'total_refunds': rounded_amount_refunds,
    'total_secures_social' : rounded_amount_secures_social,
    'total_social_tips': rounded_amount_social_tips,
    'total_taxes_pr': rounded_amount_taxes_pr,
    'total_time_worker': 0,
    'year_active': yearActive,
  }

  return data
