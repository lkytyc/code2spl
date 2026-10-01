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

class BankAccountTestDeposit(unittest.TestCase):

    def test_deposit(self):
        account1 = BankAccount()
        ret = account1.deposit(1000)
        self.assertEqual(ret, 1000)

    def test_deposit_2(self):
        account1 = BankAccount()
        account1.deposit(1000)
        ret = account1.deposit(2000)
        self.assertEqual(ret, 3000)


    def test_deposit_3(self):
        account1 = BankAccount()
        with self.assertRaises(ValueError) as context:
            account1.deposit(-1000)
        self.assertEqual(str(context.exception), "Invalid amount")

    def test_deposit_4(self):
        account1 = BankAccount()
        ret = account1.deposit(0)
        self.assertEqual(ret, 0)

    def test_deposit_5(self):
        account1 = BankAccount()
        account1.deposit(1000)
        ret = account1.deposit(1000)
        self.assertEqual(ret, 2000)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
