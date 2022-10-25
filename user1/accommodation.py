from utils.classes.payment_classes import Transaction, Money
from utils.functions.general_functions import return_council_tax

number_of_tenants = 3

list_of_accommodation_transactions = [
    Transaction(name='rent', money=-500 * 12, date_normal='10'),
    Transaction(
        name='leckie',
        money=-50 * 12,
        date_normal='4'
    ),
    Transaction(
        name='council tax',
        money=-return_council_tax(
            band='F', #discoverable on https://www.saa.gov.uk/
            number_of_tenants=number_of_tenants
        ),
        money_per_date =-89,
        date_normal='3'
    ),
    Transaction(
        name='wifi',
        money=-(24) * 12,
        regularity_of_transaction='month'
    )
]

accommodation = Money(sum([transaction.money_dict['year'] for transaction in list_of_accommodation_transactions]))

5
