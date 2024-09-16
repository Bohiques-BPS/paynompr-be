from models.queries.queryUtils import getCompany, getEmployers7000, getEmployees, getAmountVariosCompany, roundedAmount, getAmountVariosCompanyGroupByMonth, getTotalAmountAndExemptAmount
from utils.time_func import getPeriodTime

def queryForm499(company_id, year, period):
    try:
        # Data Active
        company = getCompany(company_id)['company']
        date_period = getPeriodTime(period, year)

        amountVariosExempt = getTotalAmountAndExemptAmount(company.id, date_period)
        employers = getEmployees(company.id)
        amountVarios = getAmountVariosCompany(company.id, year, period)
        amountVariosByMonth = getAmountVariosCompanyGroupByMonth(company.id, year, period)

        # Address Company
        physicalAddressCompany = company.physical_address if company.physical_address is not None else ''
        statePhysicalAddressCompany = company.state_physical_address if company.state_physical_address is not None else ''
        countryPhysicalAddressCompany = company.country_physical_address if company.country_physical_address is not None else ''


        # Calculate
        rounded_amount_bonus = roundedAmount(amountVarios.bonus)
        rounded_amount_wages = roundedAmount(amountVariosExempt['total'] + rounded_amount_bonus)
        rounded_amount_commissions = roundedAmount(amountVarios.commissions)
        rounded_amount_concessions = roundedAmount(amountVarios.concessions)
        rounded_amount_tips = roundedAmount(amountVarios.tips)
        total_salary_compensation = roundedAmount(rounded_amount_commissions + rounded_amount_wages + rounded_amount_concessions + rounded_amount_tips)
        total_retentions = roundedAmount(amountVarios.taxes_pr)

        # Part 3 Page 2 calculation
        month_total_liabilities = []
        for index, amount in enumerate(amountVariosByMonth):
            index += 1
            total = roundedAmount(amount.taxes_pr)
            mitad = total / 2
            dataTmp = {
                'total': str(total),
            }
            if total_retentions <= 2500:
                dataTmp['text_month_3_day_28'] = str(total)
                dataTmp['text_month_3_liability'] = str(total)
            elif total_retentions >= 2500 and total_retentions <= 100000:
                dataTmp[f'text_month_{index}_day_28'] = str(total)
                dataTmp[f'text_month_{index}_liability'] = str(total)
            else:
                dataTmp[f'text_month_{index}_day_14'] = str(mitad)
                dataTmp[f'text_month_{index}_day_28'] = str(mitad)
                dataTmp[f'text_month_{index}_liability'] = str(total)

            month_total_liabilities.append(dataTmp)

        # Data for PDF
        data = {
            'text_name_company': company.name if company.name is not None else '', # company name
            'text_ein': company.number_patronal if company.number_patronal is not None else '', # company ein
            'text_name_contact' : company.contact if company.contact is not None else '', # contact name
            'text_phone_company': str(company.phone_number) if company.phone_number is not None else '', # company phone number
            'personal_contact_number': str(company.contact_number) if company.contact_number is not None else '', # personal contact number
            'textarea_address_company': f'{physicalAddressCompany} \n {statePhysicalAddressCompany} {countryPhysicalAddressCompany}', # address company
            'text_total_employees': str(len(employers)), # total number of employees
            'text_total_exempt': str(amountVariosExempt['exempt']), # total exempt
            'text_total_compensation_withholding': str(total_salary_compensation), # total salary compensation
            'text_total_tips_withholding': str(rounded_amount_tips), # total tip compensation
            'text_total_withholding': str(total_retentions), # total retentions
            'text_total_quarter_liability': str(total_retentions), # total retentions
            'text_first_month_liability': month_total_liabilities[0]['total'] if len(month_total_liabilities) > 0 else '0',
            'text_second_month_liability': month_total_liabilities[1]['total'] if len(month_total_liabilities) > 1 else '0',
            'text_third_month_liability': month_total_liabilities[2]['total'] if len(month_total_liabilities) > 2 else '0',
            'text_total_liability_quarter': str(total_retentions), # total retentions
        }

        for value in month_total_liabilities:
            data.update(value)


        return data
    except Exception as e:
        print(f'Error in queryForm499: {str(e)}')
        return None



