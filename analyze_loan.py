#IMPORTS
import datetime as dt
from dateutils import relativedelta
import matplotlib.pyplot as plt
import numpy_financial as npf
import pandas as pd

#CLASS
class Loan:

    #INITIALIZER
    #rate = interest rate
    #term = term of loan in years
    #loan_amount = amount of loan
    #start_date = date loan starts; deafults to today and isoformat is used to convert to string

    def __init__(self, rate, term, loan_amount, start_date=dt.date.today().isoformat()):
        self.rate = rate / 1200
        self.periods = term * 12
        self.loan_amount = loan_amount
        # month_start_date is a function that takes a date and returns the first day of the month; most common for loans
        self.start_date = relativedelta(day=1, months=+1)+dt.date.fromisoformat(start_date)
        # pmt is the monthly payment amount
        self.pmt = npf.pmt(self.rate, self.periods, -self.loan_amount)
        # pmt_str is the monthly payment amount formatted as a string
        self.pmt_str = f"${self.pmt:,.2f}"
        self.table = self.loan_table()
    
    # METHODS

    # loan_table returns a dataframe with the loan payment, interest, principal, and balance for each month
    def loan_table(self):
        
        # enumerate the periods from the start date to the end date
        periods = [self.start_date + relativedelta(months=x) for x in range(self.periods)]
        
        # interest is the interest paid for each month and principal is the principal paid for each month
        interest = [npf.ipmt(self.rate, month, self.periods, -self.loan_amount)
                    for month in range(1, self.periods + 1)]
        principal = [npf.ppmt(self.rate, month, self.periods, -self.loan_amount)
                     for month in range(1, self.periods + 1)]
        
        # create a dataframe with the payment, interest, and principal
        table = pd.DataFrame({'Payment': self.pmt,
                              'Interest': interest,
                              'Principal': principal}, 
                              index=pd.to_datetime(periods))
        
        # balance is the loan balance after each payment
        table['Balance'] = self.loan_amount - table['Principal'].cumsum()
        return table.round(2)

    # plot_balances plots the loan balance and interest paid over time
    def plot_balances(self):
        amort = self.loan_table()
        plt.plot(amort.Balance, label='Balance')
        plt.plot(amort.Interest.cumsum(), label='Interest Paid')
        plt.grid(axis='y', alpha=.5)
        plt.legend(loc=8)
        plt.show()

    # summary prints a summary of the loan
    def summary(self):
        amort = self.table
        print("Summary")
        print("-" * 30)
        print(f'Payment: {self.pmt_str:>21}')
        print(f'{"Payoff Date:":19s} {amort.index.date[-1]}')
        print(f'Interest Paid: {amort.Interest.cumsum()[-1]:>15,.2f}')
        print("-" * 30)

    # pay_early returns the number of years to pay off the loan if you pay extra_amt each month
    def pay_early(self, extra_amt):
        return f'{round(npf.nper(self.rate, self.pmt + extra_amt, -self.loan_amount) / 12, 2)}'

    # retire_debt returns the extra payment and payment amount needed to pay off the loan in years_to_debt_free years
    def retire_debt(self, years_to_debt_free):
        extra_pmt = 1
        while npf.nper(self.rate, self.pmt + extra_pmt, -self.loan_amount) / 12 > years_to_debt_free:
            extra_pmt += 1
        return extra_pmt, self.pmt + extra_pmt
    
loan = Loan(5.875, 30, 360000)
print(loan.table)
# amort = loan.table
# loan.plot_balances()
# print(amort)
# print(loan.retire_debt(10))
# print(loan.pay_early(100))
# loan.summary()