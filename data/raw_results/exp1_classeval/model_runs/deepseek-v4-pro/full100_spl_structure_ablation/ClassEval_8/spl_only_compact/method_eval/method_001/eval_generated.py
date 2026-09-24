class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        if amount < 0:
            print("Invalid amount")
            raise ValueError("Raised when amount is negative.")
        self.balance += amount
        return self.balance

    def transfer(self, other_account, amount):
        withdraw_result = self.withdraw(amount)
        deposit_result = other_account.deposit(amount)

    def view_balance(self):
        return self.balance

    def withdraw(self, amount):
        if amount < 0:
            print("Invalid amount")
            raise ValueError("Raised when the requested withdrawal amount is negative.")
        if amount > self.balance:
            print("Insufficient balance.")
            raise ValueError("Raised when the requested withdrawal amount exceeds the current balance.")
        self.balance -= amount
        return self.balance

import unittest

class BankAccountTestWithdraw(unittest.TestCase):

    def test_withdraw(self):
        account1 = BankAccount()
        account1.balance = 1000
        ret = account1.withdraw(200)
        self.assertEqual(ret, 800)

    def test_withdraw_2(self):
        account1 = BankAccount()
        account1.balance = 500
        with self.assertRaises(ValueError) as context:
            account1.withdraw(1000)
        self.assertEqual(str(context.exception), "Insufficient balance.")

    def test_withdraw_3(self):
        account1 = BankAccount()
        with self.assertRaises(ValueError) as context:
            account1.withdraw(-1000)
        self.assertEqual(str(context.exception), "Invalid amount")

    def test_withdraw_4(self):
        account1 = BankAccount()
        account1.balance = 1000
        ret = account1.withdraw(500)
        self.assertEqual(ret, 500)

    def test_withdraw_5(self):
        account1 = BankAccount()
        account1.balance = 1000
        ret = account1.withdraw(1000)
        self.assertEqual(ret, 0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
