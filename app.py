from analyze_loan import Loan
import sys
from time import sleep

def menu():
    print("""
    Menu
    -----------------

    0. Exit
    1. Start a new loan
    2. Show Payment
    3. Show Amortization Table
    4. Show Summary
    5. Plot Balances
    6. Add Extra Payment
    7. Retire Debt
    """)

def get_loan():
    rate = float(input("Enter the interest rate: "))
    years = int(input("Enter the number of years: "))
    amount = int(input("Enter the loan amount: "))
    loan = Loan(rate, years, amount)
    return loan

def pmt(loan):
    print(loan.pmt_str)

def amortization(loan):
    print(loan.table)

def summary(loan):
    loan.summary()

def plot_balances(loan):
    loan.plot_balances()

def extra_payment(loan):
    extra = int(input("Enter the extra payment amount: "))
    print(f'You will pay off the loan in {loan.pay_early(extra)} years.')

def retire_debt(loan):
    years = int(input("Enter the number of years to pay off the loan: "))
    extra, pmt = loan.retire_debt(years)
    print(f'You need to pay an extra {extra} each month to pay off the loan in {years} years.')
    print(f'Your new payment will be {pmt}.')

options = { 
    '0': sys.exit,
    '1': get_loan,
    '2': pmt,
    '3': amortization,
    '4': summary,
    '5': plot_balances,
    '6': extra_payment,
    '7': retire_debt
}

def main():
    while True:
        menu()
        choice = input("Enter your selection: ")
        if choice == '1':
            rate = float(input("Enter interest rate: "))
            term = int(input("Enter loan term: "))
            pv = float(input("Enter amount borrowed: "))
            loan = Loan(rate, term, pv)
            print("Loan initialized")
            sleep(.75)

        elif choice in '234567':
            try:
                options[choice](loan)
                sleep(2)
            except NameError:
                print("No Loan setup")
                print("Set up a new loan")
                sleep(2)

        elif choice == '0':
            print("Goodbye")
            sys.exit()
        else:
            print("please enter a valid selection")

if __name__ == "__main__":
    main()