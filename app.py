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

def main():
    menu()

if __name__ == "__main__":
    main()