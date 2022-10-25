import re


class Money:
    def __init__(self, money):
        self.money_dict = {
            'year': money,
            'month': money / 12,
            'week': money / 52
        }


class Transaction(Money):
    def __init__(self, name='', money=0, money_per_date=None, regularity_of_transaction=None,
                 date_normal=None, nation='scotland', delayed_by_weekend=True, delayed_by_bank_holiday=True
                 ):
        super().__init__(money)
        if not date_normal and not regularity_of_transaction:
            raise Exception('transactions without a date_normal need regularity_of_transaction specified')
        self.name = name
        self.nation = nation
        self.delayed_by_weekend = delayed_by_weekend
        self.delayed_by_bank_holiday = delayed_by_bank_holiday
        self.date_normal = date_normal
        self.date_actual = None
        if date_normal:
            if self.is_date_valid(date_normal):
                self.date_normal = date_normal.upper()
                self.date_actual = self.date_normal
        if not regularity_of_transaction:
            self.update_regularity_of_transaction()
        else:
            self.regularity_of_transaction = regularity_of_transaction
        if not money_per_date:
            self.money_per_date = self.money_dict[self.regularity_of_transaction]
        else:
            self.money_per_date = money_per_date

    def is_date_valid(self, date):

        valid_weekdays = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']

        def date_day_is_valid(list_of_date_numbers):
            if int(list_of_date_numbers[0]) <= 31:
                return True

        def date_day_and_month_is_valid(list_of_date_numbers):
            if date_day_is_valid(list_of_date_numbers) and int(list_of_date_numbers[1]) <= 12:
                return True

        def date_day_and_month_and_year_is_valid(list_of_date_numbers):
            if date_day_and_month_is_valid(list_of_date_numbers) and len(list_of_date_numbers[2]) == 4:
                return True

        if type(date) == str:
            date = date.strip()
            if re.search('[0-9]+', date):
                # inputted date consists solely of numbers
                list_of_date_numbers = date.split()
                if len(list_of_date_numbers) > 3:
                    raise Exception('the inputted date has too many numbers')
                if len(list_of_date_numbers) == 1 and date_day_is_valid(list_of_date_numbers):
                    return True
                elif len(list_of_date_numbers) == 2 and date_day_and_month_is_valid(list_of_date_numbers):
                    return True
                elif len(list_of_date_numbers) == 3 and date_day_and_month_and_year_is_valid(list_of_date_numbers):
                    return True
                else:
                    raise Exception('the inputted date is invalid')
            else:
                # inputted date does not soley consist of numbers
                date = date.upper()
                input_is_valid = False
                for valid_weekday in valid_weekdays:
                    if date == valid_weekday:
                        input_is_valid = True
                        break
                if input_is_valid:
                    return True
                else:
                    raise Exception('the inputted date is invalid')
        else:
            raise Exception('the inputted date was not a string')

    def update_regularity_of_transaction(self):
        if re.search('[0-9]+', self.date_actual):
            list_of_numbers = self.date_actual.split()
            if len(list_of_numbers) == 1:
                self.regularity_of_transaction = 'month'
            elif len(list_of_numbers) == 2:
                self.regularity_of_transaction = 'year'
            elif len(list_of_numbers) == 3:
                self.regularity_of_transaction = 'one off'
        else:
            self.regularity_of_transaction = 'week'

    def add_date(self, date):
        if self.is_date_valid(date):
            self.date_normal = date.upper()
            self.date_actual = date.upper()
            self.update_regularity_of_transaction()

    def update_date_actual(self, date):
        if self.is_date_valid(date):
            self.date_actual = date.upper()
            self.update_regularity_of_transaction()


class SalaryTransaction(Transaction):
    def __init__(self, money, days_per_week, hours_per_week, pensionable_income, ni_category_letter, nation='scotland',
                 date_normal=None, name='',
                 pension_employee_contribution_rate=0.05,  # Found in Ito handbook and bamboo
                 pension_employer_contribution_rate=0.03  # Found in Ito handbook and bamboo
                 ):
        super().__init__(money=money, name=name, date_normal=date_normal, nation=nation)

        self.money_dict.update(
            {
                'day': self.money_dict['week'] / days_per_week,
                'hour': self.money_dict['week'] / hours_per_week
            }
        )
        self.ni_category_letter = ni_category_letter
        self.pension_contribution_employee_dictionary = {'year': pensionable_income * pension_employee_contribution_rate}
        self.pension_contribution_employee_dictionary['month'] = (self.pension_contribution_employee_dictionary['year']) / 12
        self.pension_contribution_employer_dictionary = {'year': pensionable_income * pension_employer_contribution_rate}
        self.pension_contribution_employer_dictionary['month'] = self.pension_contribution_employer_dictionary['year'] / 12
        self.ni_employee_dictionary = {'month': self.return_ni_employee_monthly()}
        self.ni_employee_dictionary['year'] = (self.ni_employee_dictionary['month']) * 12
        self.ni_employer_dictionary = {'month': self.return_ni_employer_monthly()}
        self.ni_employer_dictionary['year'] = (self.ni_employer_dictionary['month']) * 12
        self.income_tax_dictionary = {'year': self.return_income_tax()}
        self.income_tax_dictionary['month'] = (self.income_tax_dictionary['year']) / 12
        self.deductions_dictionary = {'year': self.income_tax_dictionary['year'] + self.ni_employee_dictionary['year'] + self.pension_contribution_employee_dictionary['year']}
        self.deductions_dictionary['month'] = self.deductions_dictionary['year'] / 12
        self.money_dict.update(
            {
                'after tax': {
                    'year': self.money_dict['year'] - self.deductions_dictionary['year'],
                    'month': self.money_dict['month'] - self.deductions_dictionary['month']
                }
            }
        )
        self.money_per_date = self.money_dict['after tax']['month']

    def return_ni_employee_monthly(self):
        '''
        https://www.gov.uk/national-insurance-rates-letters
        '''
        assert self.ni_category_letter.lower() == 'a', 'we need to program for NI category letter to be something other than A!'

        ni_employee_monthly = 0

        band2_dictionary = {
            'threshold': 1048,
            'tax_rate': 0.1325
        }
        band3_dictionary = {
            'threshold': 4189,
            'tax_rate': 0.0325
        }

        if self.money_dict['month'] > band3_dictionary['threshold']:
            band3_taxable_income = self.money_dict['month'] - band3_dictionary['threshold']
            ni_employee_monthly += band3_taxable_income * band2_dictionary['tax_rate']

        if self.money_dict['month'] > band2_dictionary['threshold']:
            if self.money_dict['month'] > band3_dictionary['threshold']:
                band2_taxable_income = band3_dictionary['threshold'] - band2_dictionary['threshold']
            else:
                band2_taxable_income = self.money_dict['month'] - band2_dictionary['threshold']
            ni_employee_monthly += band2_taxable_income * band2_dictionary['tax_rate']

        return ni_employee_monthly

    def return_ni_employer_monthly(self):
        '''
        https://www.gov.uk/national-insurance-rates-letters
        '''
        assert self.ni_category_letter.lower() == 'a', 'we need to program for NI category letter to be something other than A!'

        ni_employer_monthly = 0
        band2_dictionary = {
            'threshold': 758,
            'tax_rate': 0.1505
        }
        band3_dictionary = {
            'threshold': 2083,
            'tax_rate': 0.1505
        }
        band4_dictionary = {
            'threshold': 4189,
            'tax_rate': 0.1505
        }

        if self.money_dict['month'] > band4_dictionary['threshold']:
            band4_taxable_ni_monthly = self.money_dict['month'] - band4_dictionary['threshold']
            ni_employer_monthly += band4_taxable_ni_monthly * band4_dictionary['tax_rate']

        if self.money_dict['month'] > band3_dictionary['threshold']:
            if self.money_dict['month'] > band4_dictionary['threshold']:
                band3_taxable_ni_monthly = band4_dictionary['threshold'] - band3_dictionary['threshold']
            else:
                band3_taxable_ni_monthly = self.money_dict['month'] - band3_dictionary['threshold']
            ni_employer_monthly += band3_taxable_ni_monthly * band3_dictionary['tax_rate']

        if self.money_dict['month'] > band2_dictionary['threshold']:
            if self.money_dict['month'] > band3_dictionary['threshold']:
                band2_taxable_ni_monthly = band3_dictionary['threshold'] - band2_dictionary['threshold']
            else:
                band2_taxable_ni_monthly = self.money_dict['month'] - band2_dictionary['threshold']
            ni_employer_monthly += band2_taxable_ni_monthly * band2_dictionary['tax_rate']

        return ni_employer_monthly

    def return_income_tax(self):
        '''
        https://www.gov.uk/scottish-income-tax
        https://www.tax.service.gov.uk/estimate-paye-take-home-pay/your-pay
        '''
        income_tax = 0
        starter_dictionary = {
            'threshold': 12571,
            'tax_rate': 0.19
        }
        basic_dictionary = {
            'threshold': 14733,
            'tax_rate': 0.2
        }
        intermediate_dictionary = {
            'threshold': 25689,
            'tax_rate': 0.21
        }
        high_dictionary = {
            'threshold': 43663,
            'tax_rate': 0.41
        }
        top_dictionary = {
            'threshold': 150000,
            'tax_rate': 0.46
        }

        if self.money_dict['year'] > top_dictionary['threshold']:
            top_rate_taxable_income = self.money_dict['year'] - top_dictionary['threshold']
            income_tax += top_rate_taxable_income * top_dictionary['tax_rate']

        if self.money_dict['year'] > high_dictionary['threshold']:
            higher_rate_taxable_income = self.money_dict['year'] - high_dictionary['threshold']
            if self.money_dict['year'] > top_dictionary['threshold']:
                higher_rate_taxable_income = top_dictionary['threshold'] - high_dictionary['threshold']
            income_tax += higher_rate_taxable_income * high_dictionary['tax_rate']

        if self.money_dict['year'] > intermediate_dictionary['threshold']:
            intermediate_rate_taxable_income = self.money_dict['year'] - intermediate_dictionary['threshold']
            if self.money_dict['year'] > high_dictionary['threshold']:
                intermediate_rate_taxable_income = high_dictionary['threshold'] - intermediate_dictionary['threshold']
            income_tax += intermediate_rate_taxable_income * intermediate_dictionary['tax_rate']

        if self.money_dict['year'] > basic_dictionary['threshold']:
            basic_rate_taxable_income = self.money_dict['year'] - basic_dictionary['threshold']
            if self.money_dict['year'] > intermediate_dictionary['threshold']:
                basic_rate_taxable_income = intermediate_dictionary['threshold'] - basic_dictionary['threshold']
            income_tax += basic_rate_taxable_income * basic_dictionary['tax_rate']

        if self.money_dict['year'] > starter_dictionary['threshold']:
            starter_rate_taxable_income = self.money_dict['year'] - starter_dictionary['threshold']
            if self.money_dict['year'] > basic_dictionary['threshold']:
                starter_rate_taxable_income = basic_dictionary['threshold'] - starter_dictionary['threshold']
            income_tax += starter_rate_taxable_income * starter_dictionary['tax_rate']

        return income_tax









