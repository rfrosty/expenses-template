from utils.classes.payment_classes import Transaction, Money, SalaryTransaction

list_of_taxed_incomes = [
    SalaryTransaction(
        name='the government',
        money=30000, # payslip's monthly pay (2354.33) * 12
        days_per_week=5,
        nation='england',
        date_normal='26', #'26 5 2022',
        hours_per_week=37.5,
        pensionable_income=23760, # derived from this site: https://www.moneyhelper.org.uk/en/pensions-and-retirement/auto-enrolment/use-our-workplace-pension-calculator#
        ni_category_letter='a', # payslip's National Insurance Table.
   )
]

list_of_untaxed_incomes = [
    Transaction(name='untaxed income 1', money=200 * 12, regularity_of_transaction='month')
]

total_taxed_income = Money(sum([transaction.money_dict['year'] for transaction in list_of_taxed_incomes]))
total_taxed_income_after_tax = Money(sum(transaction.money_dict['after tax']['year'] for transaction in list_of_taxed_incomes))
total_untaxed_income = Money(sum(transaction.money_dict['year'] for transaction in list_of_untaxed_incomes))
total_taxed_income_after_tax_plus_total_untaxed_income = Money(total_taxed_income_after_tax.money_dict['year'] + total_untaxed_income.money_dict['year'])
total_income = Money(total_taxed_income.money_dict['year'] + total_untaxed_income.money_dict['year'])

5