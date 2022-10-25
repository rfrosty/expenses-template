from income import list_of_taxed_incomes, list_of_untaxed_incomes
from user1.accommodation import list_of_accommodation_transactions
from user1.subscriptions import list_of_subscription_transactions
from user1.spending import list_of_spending_transactions
from utils.classes.calendar_classes import Timeframe
from datetime import datetime

transactions = list_of_taxed_incomes + list_of_untaxed_incomes + list_of_accommodation_transactions + list_of_subscription_transactions + list_of_spending_transactions

timeframe1 = Timeframe(0, transactions, sdatetime=datetime(2022, 10, 1), edatetime=datetime(2022, 11, 1))

print('end')





