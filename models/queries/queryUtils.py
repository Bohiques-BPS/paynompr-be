from models.companies import Companies
from models.employers import Employers
from models.periods import Period
from models.time import Time
from database.config import session
from random import randint
from models.accountant import Accountant
from sqlalchemy import func, and_
from datetime import date
from utils.time_func import getPeriodTime, getAgeEmployer

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


def getTotalAmountAndExemptAmount(company_id, date_period):
    result = session.query(func.sum(Time.total_payment).label('total'), Employers.id, Employers.birthday).join(Employers).join(Period).filter(
      and_(
        Employers.company_id == company_id,
        Period.period_start >= date_period['start'],
        Period.period_end <= date_period['end']
      )
    ).group_by(Employers.id).all()

    total = 0
    exempt_amount = 0
    for payment in result:
      total += payment[0]
      if payment[2] is not None:
        birthday = str(payment[2]).split('-') if payment[2] is not None else '0000-00-00'.split('-')
        age = getAgeEmployer(birthday)
        if age > 26:
          exempt_amount += payment[0]

    total_amount = total - exempt_amount
    return {
      'total': total_amount,
      'exempt': exempt_amount
    }


def getTotalAmount(company_id, date_period):
    result = session.query(func.sum(Time.total_payment)).join(Employers, Period).filter(
      and_(
        Employers.company_id == company_id,
        Period.period_start >= date_period['start'],
        Period.period_end <= date_period['end']
      )
    ).scalar()

    return result if result is not None else 0

def getTotalAmountAndWeeks(company_id, year, periodo):
    period = getPeriodTime(periodo, year)
    diferent = period['end'] - period['start']
    weeks = diferent.days // 7

    result = session.query(func.sum(Time.total_payment)).join(Employers, Period).filter(
      and_(
        Employers.company_id == company_id,
        Period.period_start >= period['start'],
        Period.period_end <= period['end']
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
      func.sum(Time.aflac).label('aflac'),
      func.sum(Time.medicare).label('medicares'),
      func.sum(Time.bonus).label('bonus'),
      func.sum(Time.social_tips).label('social_tips'),
      func.sum(Time.secure_social).label('secure_social'),
      func.sum(Time.tax_pr).label('taxes_pr')
      ).join(Period).filter(
        and_(
          Time.employer_id == employer_id,
          Period.period_start >= date_start,
          Period.period_end <= date_end
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
      ).join(Period).filter(
        and_(
          Employers.company_id == company_id,
          Period.period_start >= date_start,
          Period.period_end <= date_end
        )
      ).all()

    return result[0]


def getAmountVariosCompanyGroupByMonth(company_id, year, period = None):
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
      func.sum(Time.tax_pr).label('taxes_pr'),
      func.date_trunc('month', Period.period_end).label('month'),
      ).join(Period).filter(
        and_(
          Employers.company_id == company_id,
          Period.period_start >= date_start,
          Period.period_end <= date_end
        )
      ).group_by(func.date_trunc('month', Period.period_end)).order_by(func.date_trunc('month', Time.created_at)).all()

    return result

def getEmployers7000(company_id, date_period):
    arrayTotal = session.query(func.sum(Time.total_payment).label('total')).join(Employers).join(Period).filter(
      and_(
        Employers.company_id == company_id,
        Period.period_start >= date_period['start'],
        Period.period_end <= date_period['end']
      )
    ).group_by(Time.employer_id).all()
    result = 0
    for value in arrayTotal:
        max_7000 = (value.total - 7000) if value.total > 7000 else value.total
        result += max_7000

    return result

def getEmployersAmount(company_id, date_period):
    arrayTotal = session.query(
      func.sum(Time.total_payment).label('total'),
      Employers.id,
      Employers.first_name,
      Employers.last_name,
      Employers.social_security_number,
      func.date_trunc('month', Period.period_end).label('month')
    ).join(Employers).join(Period).filter(
      and_(
        Employers.company_id == company_id,
        Period.period_start >= date_period['start'],
        Period.period_end <= date_period['end']
      )
    ).group_by(Employers.id, func.date_trunc('month', Period.period_end).label('month')).all()

    return arrayTotal

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
    return employers

def getEmployer(employer_id):
    employer = session.query(Employers).filter(Employers.id == employer_id).first()
    company = session.query(Companies).filter(Companies.id == employer.company_id).first()
    return {
      'employer': employer,
      'company': company
    }