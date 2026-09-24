class BankAccount:
    """A simple bank account with deposit, withdrawal, and transfer support."""

    def __init__(self, initial_balance=0):
        self.balance = initial_balance

    def deposit(self, amount):
        """Add amount to balance. Raises ValueError for negative amounts."""
        if amount < 0:
            raise ValueError(f"Deposit amount must be non-negative, got {amount}")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        """Subtract amount from balance. Raises ValueError for negative amounts
        or amounts exceeding the current balance."""
        if amount < 0:
            raise ValueError(f"Withdrawal amount must be non-negative, got {amount}")
        if amount > self.balance:
            raise ValueError(
                f"Insufficient funds: cannot withdraw {amount} from balance of {self.balance}"
            )
        self.balance -= amount
        return self.balance

    def get_balance(self):
        """Return the current balance without modifying it."""
        return self.balance

    @staticmethod
    def transfer(source, destination, amount):
        """Transfer amount from source account to destination account.

        Calls source.withdraw followed by destination.deposit. If withdraw raises,
        deposit is never called. If deposit raises after a successful withdraw,
        the source account remains debited with no rollback.
        """
        source.withdraw(amount)
        destination.deposit(amount)

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
