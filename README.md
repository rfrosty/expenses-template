#Intro:

This is a copy of a repo I use to determine what my balance will be on any day in the future.  
It has no UI and it's not been designed for anybody to use other than me.  
However, I have replaced my info with dummy-data & instructions so you can see how I use it.
---
#Setup:
In:
- `accommodation.py`
- `income.py`
- `spending.py`
- `subscriptions.py`

input transactions into `list of {...} transactions` variable.

Give each transaction a `money` keyword-argument of the amount of money being transferred per year. (It must be a number: positive figure if going into your account; negative figure if going out your account).

Give each transaction a `date_normal` keyword-argument if possible. This denotes the regularity of the transaction and can take one of the following values:
  - `{day_of_the_week}` as a string.
  - `{number_between_1-31}` as a string. This would denote the day of the month the transaction occurs.
  - `{number_between_1-31} {number_between_1-12}` as a string. This would denote the day of the year the transaction occurs.
  - `{number_between_1-31} {number_between_1-12} {any_number}` as a string. This would denote a one-off transaction where the last number is the year.

**Note: if you can't provide a `date_normal` keyword argument, you must provide a `regularity_of_payment` keyword-argument which can take one of the following values:**
- `'week'`
- `'month'`
- `'year'`
- `'one off'`

Also, you will be prompted to input the date when the transaction occurs. A valid value is one of the valid arguments for the `date_normal` parameter mentioned above. 

There are some other keyword-arguments present in the dummy-data that're intuitive to fill in.

---
#Uses:

###Determine balance on any day in timeframe

- In `user > main.py`, input start-date & end-date in month/day/year format.
- Place a breakpoint at the end of `main.py`.
- Run debugger.
- Observe `timeframe1 > timeframe`.

###Determine savings per week/month/year
- Place a breakpoint at the end of `saving.py`.
- Run debugger.
- Observe `saving`.

###Determine all accommodation transactions per week/month/year
- Place a breakpoint at the end of `accommodation.py`.
- Run debugger.
- Observe `accommodation`.

###Determine all spending transactions per week/month/year
- Place a breakpoint at the end of `spending.py`.
- Run debugger.
- Observe `spending`.

###Determine all subscription transactions per week/month/year
- Place a breakpoint at the end of `subscriptions.py`.
- Run debugger. 
- Observe `subscriptions`.

###Determine income variables per week/month/year
- Place a breakpoint at the end of `income.py`.
- Run debugger.
- Observe variables.
---
#Known Weaknesses/Assumptions

- Doesn't handle anything other NI letter-category than 'A'.
- Assumes only possible bank holidays are the English & Scottish bank holidays from 2022-2023.
- Assumes Edinburgh council-tax band.