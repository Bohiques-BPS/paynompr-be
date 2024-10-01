from models.queries.queryUtils import getCompany, getEmployees, getAmountVariosCompany, addDecimal,roundedAmount, getRandomIrs


def queryForm943(company_id, year, period):

    try:
        # Get company and employees
        company = getCompany(company_id)['company']
        employers = getEmployees(company.id)

        # get Ein
        ein = company.number_patronal.split('-')
        ein_part_1 = ein[0] if (len(ein) >= 1) else ''
        ein_part_2 = ein[1] if (len(ein) >= 2) else ''

        # Calculate total amount
        amount_varios_number = getAmountVariosCompany(company_id, year, period)

        # Calculate total
        total_wages = amount_varios_number.wages + amount_varios_number.commissions + amount_varios_number.concessions  + amount_varios_number.tips
        salary_security_social = addDecimal(roundedAmount(total_wages))
        tax_medicares = addDecimal(roundedAmount(amount_varios_number.medicares))
        # Calculate * 0.124 + 0.029
        salary_security_social_x_0124_number = roundedAmount(total_wages * 0.124)
        salary_security_social_x_0124 = addDecimal(salary_security_social_x_0124_number)
        tax_medicares_x_0029_number = roundedAmount(amount_varios_number.medicares * 0.029)
        tax_medicares_x_0029 = addDecimal(tax_medicares_x_0029_number)

        # Calculate total 9
        total_9_number = roundedAmount(salary_security_social_x_0124_number + tax_medicares_x_0029_number)
        total_9 = addDecimal(total_9_number)



        data = {
            ## Page 1
            ## Header fields
            'topmostSubform[0].Page1[0].NameAddress_ReadOrder[0].f1_2[0]': ein_part_1, # identification ein part 1
            'topmostSubform[0].Page1[0].NameAddress_ReadOrder[0].f1_3[0]': ein_part_2, # identification ein part 2
            'topmostSubform[0].Page1[0].NameAddress_ReadOrder[0].f1_1[0]': company.name, # Name company
            'topmostSubform[0].Page1[0].NameAddress_ReadOrder[0].f1_4[0]': '', # Commercial name company
            'topmostSubform[0].Page1[0].NameAddress_ReadOrder[0].f1_5[0]': company.physical_address, # Address company
            'topmostSubform[0].Page1[0].NameAddress_ReadOrder[0].f1_6[0]': f'{company.state_physical_address}, {company.zipcode_physical_address}', # State and ZipCode company
            ## Part 1
            'topmostSubform[0].Page1[0].f1_7[0]': str(len(employers)), # Total of employees - Line 1
            'topmostSubform[0].Page1[0].f1_8[0]': salary_security_social[0], # Salary security social part 1 - Line 2
            'topmostSubform[0].Page1[0].f1_9[0]': salary_security_social[1], # Salary security social part 2 - Line 2
            'topmostSubform[0].Page1[0].f1_10[0]': '0', # Qualified sick leave wages part 1 - Line 2a
            'topmostSubform[0].Page1[0].f1_11[0]': '00', # Qualified sick leave wages part 2 - Line 2a
            'topmostSubform[0].Page1[0].f1_12[0]': '0', # Qualified family leave wages part 1 - Line 2b
            'topmostSubform[0].Page1[0].f1_13[0]': '00', # Qualified family leave wages part 2 - Line 2b
            'topmostSubform[0].Page1[0].f1_14[0]': salary_security_social_x_0124[0], # Salary security social * 0.124 part 1 - line 3
            'topmostSubform[0].Page1[0].f1_15[0]': salary_security_social_x_0124[1], # Salary security social * 0.124 part 2 - line 3
            'topmostSubform[0].Page1[0].f1_16[0]': '0', # Qualified sick leave wages * 0.062 part 1 - Line 3a
            'topmostSubform[0].Page1[0].f1_17[0]': '00', # Qualified sick leave wages * 0.062 part 2 - Line 3a
            'topmostSubform[0].Page1[0].f1_18[0]': '0', # Qualified family leave wages * 0.062 part 1 - Line 3b
            'topmostSubform[0].Page1[0].f1_19[0]': '00', # Qualified family leave wages * 0.062 part 2 - Line 3b
            'topmostSubform[0].Page1[0].f1_20[0]': tax_medicares[0], # tax medicares part 1 - Line 4
            'topmostSubform[0].Page1[0].f1_21[0]': tax_medicares[1], # tax medicares part 2 - Line 4
            'topmostSubform[0].Page1[0].f1_22[0]': tax_medicares_x_0029[0], # tax medicares x 0.029 part 1 - Line 5
            'topmostSubform[0].Page1[0].f1_23[0]': tax_medicares_x_0029[1], # tax medicares x 0.029 part 2 - Line 5
            'topmostSubform[0].Page1[0].f1_24[0]': '0', # tax medicares additional part 1 - Line 6
            'topmostSubform[0].Page1[0].f1_25[0]': '00', # tax medicares additional part 2 - Line 6
            'topmostSubform[0].Page1[0].f1_26[0]': '0', # tax medicares additional x 0.009 part 1 - Line 7
            'topmostSubform[0].Page1[0].f1_27[0]': '00', # tax medicares additional x 0.009 part 2 - Line 7
            'topmostSubform[0].Page1[0].f1_28[0]': '0', # federal income tax withheld part - Line 8
            'topmostSubform[0].Page1[0].f1_29[0]': '00', # federal income tax withheld part - Line 8
            'topmostSubform[0].Page1[0].f1_30[0]': total_9[0], # total taxes before adjustment part 1 - Line 9
            'topmostSubform[0].Page1[0].f1_31[0]': total_9[1], # total taxes before adjustment part 2 - Line 9

        }
        return data
    except Exception as e:
        print(f"Error queryForm941: {e}")
        return []

