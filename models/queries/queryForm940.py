from models.companies import Companies
from models.employers import Employers
from models.time import Time
from database.config import session
from random import randint
from models.accountant import Accountant
from sqlalchemy import func


def addZeroNumber(value):
    return f'{value}0' if len(value) == 1 else value

def addDecimal(number):
  array = str(number).split('.') if number != 0 else '0.0'.split('.')
  if len(array) == 1:
    array.append('00')
  else:
    array[1] = addZeroNumber(array[1])

  return array


def getTotalAmount(company_id):
    return session.query(func.sum(Time.total_payment)).join(Employers).filter(Employers.company_id == company_id).scalar()

def getEmployers7000(company_id):
    arrayTotal = session.query(func.sum(Time.total_payment).label('total')).join(Employers).filter(Employers.company_id == company_id).group_by(Time.employer_id).having(func.sum(Time.total_payment) >= 5000).all()
    result = 0
    for value in arrayTotal:
        result += value.total

    return result

def roundedAmount(amount, decimal = 2):
    return round(amount, decimal)

def queryForm940():
    # Data Active
    company = session.query(Companies).filter(Companies.id == 1).first()
    employer = session.query(Employers).filter(Companies.id == 1).first()
    account = session.query(Accountant).filter(Companies.id == 1).first()
    # Total amount employees
    total_amount_employers_number = roundedAmount(getTotalAmount(company.id))
    total_amount_employers = addDecimal(total_amount_employers_number)
    # total Futa
    futa_tax_number = roundedAmount(((total_amount_employers_number / 100) * 0.06, 2))
    futa_tax = addDecimal(futa_tax_number)
    # total exceeded 7000
    payment_exceeded_7000_number = roundedAmount(getEmployers7000(company.id))
    payment_exceeded_7000 = addDecimal(payment_exceeded_7000_number)
    # Linea 6
    subTotalLinea6_number = roundedAmount((payment_exceeded_7000_number + futa_tax_number))
    subTotalLinea6 = addDecimal(subTotalLinea6_number)
    # Linea 7
    salaryFuta_number = roundedAmount((total_amount_employers_number - subTotalLinea6_number))
    salaryFuta = addDecimal(salaryFuta_number)
    # Linea 8
    subTotalLinea8_number = roundedAmount((salaryFuta_number * 0.006))
    subtotalLinea8 = addDecimal(subTotalLinea8_number)
    # Linea 9
    subtotalLinea9_number = roundedAmount((salaryFuta_number * 0.054))
    subtotalLinea9 = addDecimal(subtotalLinea9_number)
    # Linea 10
    subtotalLinea10_number = 0
    subtotalLinea10 = addDecimal(subtotalLinea10_number)
    # Linea 11
    subtotalLinea11_number = 0
    subtotalLinea11 = addDecimal(subtotalLinea11_number)
    # Linea 12
    subtotalLinea12_number = roundedAmount((subTotalLinea8_number + subtotalLinea9_number + subtotalLinea10_number + subtotalLinea11_number))
    subtotalLinea12 = addDecimal(subtotalLinea12_number)
    # Linea 13
    subtotalLinea13_number = 0
    subtotalLinea13 = addDecimal(subtotalLinea13_number)
    # Linea 14
    subtotalLinea14_number = roundedAmount((subtotalLinea13_number - subtotalLinea12_number)) if subtotalLinea13_number > subtotalLinea12_number else 0
    subtotalLinea14 = addDecimal(subtotalLinea14_number)
    # Linea 15
    subtotalLinea15_number = roundedAmount((subtotalLinea13_number - subtotalLinea12_number)) if subtotalLinea13_number > subtotalLinea12_number else 0
    subtotalLinea15 = addDecimal(subtotalLinea15_number)
    # Linea 16
    trimestre1_number = 0
    trimestre1 = addDecimal(trimestre1_number)
    trimestre2_number = 0
    trimestre2 = addDecimal(trimestre2_number)
    trimestre3_number = 0
    trimestre3 = addDecimal(trimestre3_number)
    trimestre4_number = 0
    trimestre4 = addDecimal(trimestre4_number)
    # Linea 17
    subtotalLinea17_number = roundedAmount((trimestre1_number + trimestre2_number + trimestre3_number + trimestre4_number))
    subtotalLinea17 = addDecimal(subtotalLinea17_number)
    # Personal number id
    personal_number_id = str(randint(10000, 99999))
    # Number Identifier Employer
    ein = company.number_patronal.split('-')
    data = {
      'ein_first_part': ein[0],
      'ein_second_part': ein[1],
      'legal_name': company.name,
      'comercial_name': '',
      'address': company.postal_address,
      'city': company.state_postal_addess,
      'state': company.state_physical_address,
      'zip': company.zipcode_physical_address,
      'foering_country_name': company.country_physical_address,
      'province_name': company.state_physical_address,
      'postal_code': company.zipcode_postal_address,
      ## part 1
      'abreviation_state_1': company.state_physical_address[0],
      'abreviation_state_2': company.state_physical_address[1],
      ## part 2
      'total_payments_for_all_employees_1': total_amount_employers[0],
      'total_payments_for_all_employees_2': total_amount_employers[1],
      'Futa_tax_1': futa_tax[0],
      'Futa_tax_2': futa_tax[1],
      'payments_exceeded_7000_1': payment_exceeded_7000[0],
      'payments_exceeded_7000_2': payment_exceeded_7000[1],
      'total_payments_1': subTotalLinea6[0],
      'total_payments_2': subTotalLinea6[1],
      'total_futa_salary_1': salaryFuta[0],
      'total_futa_salary_2': salaryFuta[1],
      'futa_tax_before_adjustment_1': subtotalLinea8[0],
      'futa_tax_before_adjustment_2': subtotalLinea8[1],
      ## part 3
      'futa_field_9_1': subtotalLinea9[0],
      'futa_field_9_2': subtotalLinea9[1],
      'futa_field_10_1': subtotalLinea10[0],
      'futa_field_10_2': subtotalLinea10[1],
      'futa_field_11_1': subtotalLinea11[0],
      'futa_field_11_2': subtotalLinea11[1],
      ## part 4
      'total_futa_after_adjustment_1': subtotalLinea12[0],
      'total_futa_after_adjustment_2': subtotalLinea12[1],
      'futa_deposit_per_year_1':  subtotalLinea13[0],
      'futa_deposit_per_year_2': subtotalLinea13[1],
      'futa_due_balance_1': subtotalLinea14[0],
      'futa_due_balance_2': subtotalLinea14[1],
      'futa_ovepayments_1': subtotalLinea15[0],
      'futa_ovepayments_2': subtotalLinea15[1],
      ## part 5
      'futa_trimest_1_1': trimestre1[0],
      'futa_trimest_1_2': trimestre1[1],
      'futa_trimest_2_1': trimestre2[0],
      'futa_trimest_2_2': trimestre2[1],
      'futa_trimest_3_1': trimestre3[0],
      'futa_trimest_3_2': trimestre3[1],
      'futa_trimest_4_1': trimestre4[0],
      'futa_trimest_4_2': trimestre4[1],
      'total_tax_obligation_1': subtotalLinea17[0],
      'total_tax_obligation_2': subtotalLinea17[1],
      ## part 6
      'autorizated_person': f'{employer.first_name} {employer.last_name}',
      'authorized_person_phone': employer.phone_number,
      'personal_number_id_1': personal_number_id[0],
      'personal_number_id_2': personal_number_id[1],
      'personal_number_id_3': personal_number_id[2],
      'personal_number_id_4': personal_number_id[3],
      'personal_number_id_5': personal_number_id[4],
      'employer_personal_name': f'{account.name} {account.first_last_name}',
      'employer_position': 'Manager',
      'employer_diurn_number': account.phone,
    }

    return data

