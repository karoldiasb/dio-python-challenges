import textwrap
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
            print("\n@@@ Operation failed! Insufficient funds. @@@")

        elif amount > 0:
            self._balance -= amount
            print("\n=== Withdrawal completed successfully! ===")
            return True

        else:
            print("\n@@@ Operation failed! Invalid amount. @@@")

        return False

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print("\n=== Deposit completed successfully! ===")
        else:
            print("\n@@@ Operation failed! Invalid amount. @@@")
            return False

        return True


class CheckingAccount(Account):
    def __init__(self, number, client, limit=500, withdrawal_limit=3):
        super().__init__(number, client)
        self._limit = limit
        self._withdrawal_limit = withdrawal_limit

    def withdraw(self, amount):
        num_withdrawals = len(
            [
                transaction
                for transaction in self.history.transactions
                if transaction["type"] == Withdrawal.__name__
            ]
        )

        exceeded_limit = amount > self._limit
        exceeded_withdrawals = num_withdrawals >= self._withdrawal_limit

        if exceeded_limit:
            print("\n@@@ Operation failed! Withdrawal amount exceeds the limit. @@@")

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
    @abstractmethod
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


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDeposit
    [w]\tWithdraw
    [s]\tStatement
    [na]\tNew account
    [la]\tList accounts
    [nc]\tNew client
    [q]\tQuit
    => """
    return input(textwrap.dedent(menu))


def filter_client(ssn, clients):
    filtered_clients = [client for client in clients if client.ssn == ssn]
    return filtered_clients[0] if filtered_clients else None


def get_client_account(client):
    if not client.accounts:
        print("\n@@@ Client has no account! @@@")
        return

    print("\n=== Select an account ===")
    for i, account in enumerate(client.accounts, start=1):
        print(f"[{i}] Account {account.number} - Branch {account.branch}")

    try:
        option = int(input("Choose an account number: "))
        if 1 <= option <= len(client.accounts):
            return client.accounts[option - 1]
        else:
            print("\n@@@ Invalid option! @@@")
            return None
    except ValueError:
        print("\n@@@ Invalid input! @@@")
        return None


def deposit(clients):
    ssn = input("Enter client SSN: ")
    client = filter_client(ssn, clients)

    if not client:
        print("\n@@@ Client not found! @@@")
        return

    amount = float(input("Enter deposit amount: "))
    transaction = Deposit(amount)

    account = get_client_account(client)
    if not account:
        return

    client.perform_transaction(account, transaction)


def withdraw(clients):
    ssn = input("Enter client SSN: ")
    client = filter_client(ssn, clients)

    if not client:
        print("\n@@@ Client not found! @@@")
        return

    amount = float(input("Enter withdrawal amount: "))
    transaction = Withdrawal(amount)

    account = get_client_account(client)
    if not account:
        return

    client.perform_transaction(account, transaction)


def show_statement(clients):
    ssn = input("Enter client SSN: ")
    client = filter_client(ssn, clients)

    if not client:
        print("\n@@@ Client not found! @@@")
        return

    account = get_client_account(client)
    if not account:
        return

    print("\n================ STATEMENT ================")
    transactions = account.history.transactions

    statement = ""
    if not transactions:
        statement = "No transactions have been made."
    else:
        for transaction in transactions:
            statement += f"\n{transaction['type']}:\n\t$ {transaction['amount']:.2f}"

    print(statement)
    print(f"\nBalance:\n\t$ {account.balance:.2f}")
    print("===========================================")


def create_client(clients):
    ssn = input("Enter SSN (numbers only): ")
    client = filter_client(ssn, clients)

    if client:
        print("\n@@@ A client with this SSN already exists! @@@")
        return

    name = input("Enter full name: ")
    birth_date = input("Enter birth date (dd-mm-yyyy): ")
    address = input("Enter address (street, number - neighborhood - city/state): ")

    client = Individual(name=name, birth_date=birth_date, ssn=ssn, address=address)

    clients.append(client)

    print("\n=== Client created successfully! ===")


def create_account(account_number, clients, accounts):
    ssn = input("Enter client SSN: ")
    client = filter_client(ssn, clients)

    if not client:
        print("\n@@@ Client not found, account creation process terminated! @@@")
        return

    account = CheckingAccount.new_account(client=client, number=account_number)
    accounts.append(account)
    client.accounts.append(account)

    print("\n=== Account created successfully! ===")


def list_accounts(accounts):
    for account in accounts:
        print("=" * 100)
        print(textwrap.dedent(str(account)))


def main():
    clients = []
    accounts = []

    while True:
        option = menu()

        if option == "d":
            deposit(clients)

        elif option == "w":
            withdraw(clients)

        elif option == "s":
            show_statement(clients)

        elif option == "nc":
            create_client(clients)

        elif option == "na":
            account_number = len(accounts) + 1
            create_account(account_number, clients, accounts)

        elif option == "la":
            list_accounts(accounts)

        elif option == "q":
            break

        else:
            print("\n@@@ Invalid operation, please try again. @@@")


main()
