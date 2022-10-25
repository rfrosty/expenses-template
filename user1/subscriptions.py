from utils.classes.payment_classes import Transaction, Money

list_of_subscription_transactions = [
    Transaction(name='subscription1', money=-5 * 12, date_normal="20"),
    Transaction(name='subscription2', money=-10 * 12, date_normal="26"),
]

subscriptions = Money(sum([subscription.money_dict['year'] for subscription in list_of_subscription_transactions]))

5

