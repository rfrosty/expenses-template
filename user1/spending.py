from utils.classes.payment_classes import Transaction, Money

list_of_spending_transactions = [
    Transaction(
        name='monzo',
        money=-150 * 52,
        date_normal='Friday',
    )
]

spending = Money(sum([transaction.money_dict['year'] for transaction in list_of_spending_transactions]))

5