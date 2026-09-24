class BankAccount:
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Deposit amount must be non-negative")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("Withdrawal amount must be non-negative")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance

    def view_balance(self):
        return self.balance

    def transfer(self, amount, destination_account):
        self.withdraw(amount)
        destination_account.deposit(amount)

import unittest

class BankAccountTestTransfer(unittest.TestCase):

    def test_transfer(self):
        account1 = BankAccount()
        account2 = BankAccount()
        account1.balance = 800
        account2.balance = 1000
        account1.transfer(account2, 300)
        self.assertEqual(account1.view_balance(), 500)
        self.assertEqual(account2.view_balance(), 1300)

    def test_transfer_2(self):
        account1 = BankAccount()
        account2 = BankAccount()
        account1.balance = 500
        with self.assertRaises(ValueError) as context:
            account1.transfer(account2, 600)
        self.assertEqual(str(context.exception), "Insufficient balance.")

    def test_transfer_3(self):
        account1 = BankAccount()
        account2 = BankAccount()
        account1.balance = 500
        account2.balance = 1000
        with self.assertRaises(ValueError) as context:
            account1.transfer(account2, -600)
        self.assertEqual(str(context.exception), "Invalid amount")

    def test_transfer_4(self):
        account1 = BankAccount()
        account2 = BankAccount()
        account1.balance = 500
        account2.balance = 1000
        account1.transfer(account2, 500)
        self.assertEqual(account1.view_balance(), 0)
        self.assertEqual(account2.view_balance(), 1500)

    def test_transfer_5(self):
        account1 = BankAccount()
        account2 = BankAccount()
        account1.balance = 500
        account2.balance = 1000
        account1.transfer(account2, 200)
        self.assertEqual(account1.view_balance(), 300)
        self.assertEqual(account2.view_balance(), 1200)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
