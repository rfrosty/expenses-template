from utils.classes.payment_classes import Money
from income import total_taxed_income_after_tax, total_taxed_income_after_tax_plus_total_untaxed_income, total_income
from user1.accommodation import accommodation
from user1.subscriptions import subscriptions
from user1.spending import spending

saving = Money(
    total_taxed_income_after_tax_plus_total_untaxed_income.money_dict['year'] +
    accommodation.money_dict['year'] +
    subscriptions.money_dict['year'] +
    spending.money_dict['year']
)

print(
f'''
percentage of total taxed income after tax you're saving: {(saving.money_dict['year'] / total_taxed_income_after_tax.money_dict['year']) * 100} %
percentage of total income you're saving: {(saving.money_dict['year'] / total_income.money_dict['year']) * 100} %
percentage of total taxed income after tax plus total untaxed income you're saving: {(saving.money_dict['year'] / total_taxed_income_after_tax_plus_total_untaxed_income.money_dict['year']) * 100} %
'''
)

print(5)
