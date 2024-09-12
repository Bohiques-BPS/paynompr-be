from models.companies import Companies
from models.employers import Employers
from models.time import Time
from database.config import session
from random import randint
from models.accountant import Accountant
from sqlalchemy import func, and_
from datetime import date
from utils.time_func import getPeriodTime

def addZeroNumber(value):
    return f'{value}0' if len(value) == 1 else value

def getRandomIrs():
    return f'{randint(10000, 99999)}'

def addDecimal(number):
  array = str(number).split('.') if number != 0 else '0.0'.split('.')
  if len(array) == 1:
    array.append('00')
  else:
    array[1] = addZeroNumber(array[1])

  return array


def getTotalAmount(company_id, date_period):
    result = session.query(func.sum(Time.total_payment)).join(Employers).filter(
      and_(
        Employers.company_id == company_id,
        Time.created_at.between(date_period['start'], date_period['end'])
      )
    ).scalar()

    return result if result is not None else 0

def getTotalAmountAndWeeks(company_id, year, periodo):
    period = getPeriodTime(periodo, year)
    diferent = period['end'] - period['start']
    weeks = diferent.days // 7

    result = session.query(func.sum(Time.total_payment)).join(Employers).filter(
      and_(
        Employers.company_id == company_id,
        Time.created_at.between(period['start'], period['end'])
      )
    ).scalar()

    return {
      'total_amount': result if result is not None else 0,
      'weeks': weeks
    }

def getAmountVarios(employer_id, year, period = None):
    date_start = date(year, 1, 1)
    date_end = date(year, 12, 31)

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

def getAmountVariosCompany(company_id, year, period = None):
    date_start = date(year, 1, 1)
    date_end = date(year, 12, 31)

    if period is not None:
      period = getPeriodTime(period, year)
      date_start = period['start']
      date_end = period['end']

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
          Employers.company_id == company_id,
          Time.created_at.between(date_start, date_end)
        )
      ).all()

    return result[0]

def getEmployers7000(company_id, date_period):
    arrayTotal = session.query(func.sum(Time.total_payment).label('total')).join(Employers).filter(
      and_(
        Employers.company_id == company_id,
        Time.created_at.between(date_period['start'], date_period['end'])
      )
    ).group_by(Time.employer_id).all()
    result = 0
    for value in arrayTotal:
        max_7000 = (value.total - 7000) if value.total > 7000 else value.total
        result += max_7000

    return result

def roundedAmount(amount, decimal = 2):
    return round(amount, decimal)

def getCompany(company_id):
    company = session.query(Companies).filter(Companies.id == company_id).first()
    account = session.query(Accountant).filter(Companies.id == company.id).first()
    return {
      'company': company,
      'account': account
    }

def getEmployees(company_id):
    employers = session.query(Employers).filter(Employers.company_id == company_id).all()
    print('Employees')
    print(employers)
    return employers

def getEmployer(employer_id):
    employer = session.query(Employers).filter(Employers.id == employer_id).first()
    company = session.query(Companies).filter(Companies.id == employer.company_id).first()
    return {
      'employer': employer,
      'company': company
    }