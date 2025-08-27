from abc import ABC, abstractmethod
from datetime import datetime


class Client:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def perform_transaction(self, account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)


class Individual(Client):
    def __init__(self, name, birth_date, ssn, address):
        super().__init__(address)
        self.name = name
        self.birth_date = birth_date
        self.ssn = ssn


class Account:
    def __init__(self, number, client):
        self._balance = 0
        self._number = number
        self._branch = "0001"
        self._client = client
        self._history = History()

    @classmethod
    def new_account(cls, client, number):
        return cls(number, client)

    @property
    def balance(self):
        return self._balance

    @property
    def number(self):
        return self._number

    @property
    def branch(self):
        return self._branch

    @property
    def client(self):
        return self._client

    @property
    def history(self):
        return self._history

    def withdraw(self, amount):
        balance = self.balance
        insufficient_funds = amount > balance

        if insufficient_funds:
            print("\n@@@ Operation failed! You do not have enough balance. @@@")

        elif amount > 0:
            self._balance -= amount
            print("\n=== Withdrawal completed successfully! ===")
            return True

        else:
            print("\n@@@ Operation failed! The provided amount is invalid. @@@")

        return False

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print("\n=== Deposit completed successfully! ===")
        else:
            print("\n@@@ Operation failed! The provided amount is invalid. @@@")
            return False

        return True


class CheckingAccount(Account):
    def __init__(self, number, client, limit=500, withdrawal_limit=3):
        super().__init__(number, client)
        self.limit = limit
        self.withdrawal_limit = withdrawal_limit

    def withdraw(self, amount):
        num_withdrawals = len(
            [
                transaction
                for transaction in self.history.transactions
                if transaction["type"] == Withdrawal.__name__
            ]
        )

        exceeded_limit = amount > self.limit
        exceeded_withdrawals = num_withdrawals >= self.withdrawal_limit

        if exceeded_limit:
            print(
                "\n@@@ Operation failed! The withdrawal amount exceeds the limit. @@@"
            )

        elif exceeded_withdrawals:
            print("\n@@@ Operation failed! Maximum number of withdrawals exceeded. @@@")

        else:
            return super().withdraw(amount)

        return False

    def __str__(self):
        return f"""\
            Branch:\t\t{self.branch}
            Account:\t{self.number}
            Holder:\t\t{self.client.name}
        """


class History:
    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,
                "amount": transaction.amount,
                "date": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class Transaction(ABC):
    @property
    @abstractmethod
    def amount(self):
        pass

    @classmethod
    def register(cls, account):
        pass


class Withdrawal(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def register(self, account):
        success = account.withdraw(self.amount)

        if success:
            account.history.add_transaction(self)


class Deposit(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def register(self, account):
        success = account.deposit(self.amount)

        if success:
            account.history.add_transaction(self)
