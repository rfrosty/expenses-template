from datetime import datetime, timedelta


class Day:

    scottish_bank_holidays_2022_tax_year = [  # as found here: https://www.gov.uk/bank-holidays
        datetime(2022, 5, 2),
        datetime(2022, 6, 2),
        datetime(2022, 6, 3),
        datetime(2022, 8, 1),
        datetime(2022, 11, 30),
        datetime(2022, 12, 26),
        datetime(2022, 12, 27)
    ]

    english_bank_holidays_2022_tax_year = [  # as found here: https://www.gov.uk/bank-holidays
        datetime(2022, 5, 2),
        # datetime(2022, 5, 6), # this is a fake holiday for testing purposes
        datetime(2022, 6, 2),
        datetime(2022, 6, 3),
        datetime(2022, 8, 29),
        datetime(2022, 12, 26),
        datetime(2022, 12, 27)
    ]

    def __init__(self, datetime_obj, balance=0):
        self.datetime_obj = datetime_obj
        self.date_day = datetime_obj.strftime('%-d')
        self.date_month = datetime_obj.strftime('%-m')
        self.date_year = datetime_obj.strftime('%Y')
        self.weekday = self.datetime_obj.strftime("%A")
        self.is_weekend = self.is_weekend()
        self.bank_holiday_dict_by_nation_and_boolean = {
            'scotland': self.is_bank_holiday(self.scottish_bank_holidays_2022_tax_year),
            'england': self.is_bank_holiday(self.english_bank_holidays_2022_tax_year)
        }
        self.balance = 0
        self.transactions_that_day = {}

    def is_weekend(self):
        if self.weekday.upper() == 'SATURDAY' or self.weekday.upper() == 'SUNDAY':
            return True
        else:
            return False

    def is_bank_holiday(self, list_of_bank_holidays):
        for bank_holiday in list_of_bank_holidays:
            if self.datetime_obj == bank_holiday:
                return True
        return False


class Timeframe:

    def __init__(self, balance, transactions, sdatetime, edatetime):
        self.balance = balance
        self.transactions = transactions
        self.sdatetime = sdatetime
        self.edatetime = edatetime
        self.timeframe = self.populate_timeframe_with_days()
        self.add_date_to_transactions_with_no_date()
        self.populate_timeframe_with_transactions()
        self.timeframe_only_with_days_where_transactions_took_place = [self.timeframe[date] for date in self.timeframe if self.timeframe[date].transactions_that_day]

    def populate_timeframe_with_days(self):

        timeframe = {}

        delta = self.edatetime - self.sdatetime

        for i in range(delta.days + 1):
            date_obj = self.sdatetime + timedelta(days=i)
            day = Day(date_obj)
            key = f"{day.date_day} {day.date_month} {day.date_year}"
            timeframe.update(
                {
                    key: day
                }
            )

        return timeframe

    def add_date_to_transactions_with_no_date(self):
        for transaction in self.transactions:
            if type(transaction.date_normal) == type(None):
                if transaction.name:
                    first_communication_snippet = f'A {transaction.name}'
                else:
                    first_communication_snippet = f'An unknown'
                first_question_to_user = f'{first_communication_snippet} transaction of £{transaction.money_per_date} has no given date. Input when this transaction takes place:'
                date = input(first_question_to_user)
                transaction.add_date(date)

    def populate_timeframe_with_transactions(self):
        def populate_day_with_transactions(day, transaction):
            self.balance += transaction.money_per_date
            day.balance = self.balance
            day.transactions_that_day.update(
                {
                    f'{transaction.name}': f'{transaction.money_per_date}'
                }
            )
            transaction.update_date_actual(transaction.date_normal)

        def date_needs_delayed(day, transaction):
            def delay_transaction(day, transaction, number_of_days_to_delay):
                new_date = day.datetime_obj + timedelta(number_of_days_to_delay)
                new_date = f"{new_date.strftime('%-d')} {new_date.strftime('%-m')} {new_date.strftime('%Y')}"
                transaction.update_date_actual(new_date)

            if transaction.delayed_by_weekend:
                if day.weekday == 'Saturday':
                    delay_transaction(day, transaction, 2)
                    return True
                elif day.weekday == 'Sunday':
                    delay_transaction(day, transaction, 1)
                    return True
            for key in day.bank_holiday_dict_by_nation_and_boolean:
                if transaction.nation == key and day.bank_holiday_dict_by_nation_and_boolean[key]:
                    delay_transaction(day, transaction, 1)
                    return True

        for day in self.timeframe:
            self.timeframe[day].balance = self.balance
            for transaction in self.transactions:
                if transaction.date_actual == self.timeframe[day].weekday.upper() \
                        or transaction.date_actual == self.timeframe[day].date_day \
                        or transaction.date_actual == f"{self.timeframe[day].date_day} {self.timeframe[day].date_month}" \
                        or transaction.date_actual == f"{self.timeframe[day].date_day} {self.timeframe[day].date_month} {self.timeframe[day].date_year}":
                    if not date_needs_delayed(self.timeframe[day], transaction):
                        populate_day_with_transactions(self.timeframe[day], transaction)
