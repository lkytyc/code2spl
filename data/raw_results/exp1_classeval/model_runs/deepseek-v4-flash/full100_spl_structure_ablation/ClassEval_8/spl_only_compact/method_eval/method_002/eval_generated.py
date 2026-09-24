class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Raised when the deposit amount is negative.")
        self.balance += amount
        return self.balance

    def transfer(self, other_account, amount):
        self.withdraw(amount)
        other_account.deposit(amount)

    def view_balance(self):
        return self.balance

    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("Raised when the withdrawal amount is negative.")
        if amount > self.balance:
            raise ValueError("Raised when the withdrawal amount is greater than the current balance.")
        self.balance -= amount
        return self.balance

import unittest

class BankAccountTestViewBalance(unittest.TestCase):

    def test_view_balance(self):
        account1 = BankAccount()
        self.assertEqual(account1.view_balance(), 0)

    def test_view_balance_2(self):
        account1 = BankAccount()
        account1.balance = 1000
        self.assertEqual(account1.view_balance(), 1000)

    def test_view_balance_3(self):
        account1 = BankAccount()
        account1.balance = 500
        self.assertEqual(account1.view_balance(), 500)

    def test_view_balance_4(self):
        account1 = BankAccount()
        account1.balance = 1500
        self.assertEqual(account1.view_balance(), 1500)

    def test_view_balance_5(self):
        account1 = BankAccount()
        account1.balance = 2000
        self.assertEqual(account1.view_balance(), 2000)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
