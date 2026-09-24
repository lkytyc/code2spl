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
