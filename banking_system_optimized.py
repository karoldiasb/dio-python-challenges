import textwrap


def deposit(balance, statement):
    amount = float(input("Enter the deposit amount: "))

    if amount <= 0:
        print("Operation failed! The entered amount is invalid.")
        return balance, statement

    balance += amount
    statement += f"Deposit: $ {amount:.2f}\n"
    return balance, statement


def withdraw(balance, statement, withdrawal_count, limit, max_withdrawals):
    amount = float(input("Enter the withdrawal amount: "))

    if amount <= 0:
        print("Operation failed! The entered amount is invalid.")
        return balance, statement

    if amount > balance:
        print("Operation failed! Insufficient balance.")
        return balance, statement

    if amount > limit:
        print("Operation failed! The withdrawal amount exceeds the limit.")
        return balance, statement

    if withdrawal_count >= max_withdrawals:
        print("Operation failed! Maximum number of withdrawals exceeded.")
        return balance, statement

    balance -= amount
    statement += f"Withdrawal: $ {amount:.2f}\n"
    withdrawal_count += 1
    return balance, statement


def show_statement(balance, statement):
    print("\n========== STATEMENT ==========")
    print("No transactions have been made." if not statement else statement)
    print(f"\nBalance: $ {balance:.2f}")
    print("================================")


def filter_user(cpf, users):
    filtered_users = [user for user in users if user["cpf"] == cpf]
    return filtered_users[0] if filtered_users else None


def create_user(users):
    cpf = input("Enter your CPF (number only): ")
    user = filter_user(cpf, users)

    if user:
        print("\n@@@ There is already a user with this CPF! @@@")
        return

    users.append(
        {
            "name": input("Enter your full name: "),
            "date_of_birthday": input("Enter your date of birth (dd-mm-yyyy): "),
            "cpf": cpf,
            "address": input(
                "Enter the address (street, number - neighborhood - city/state abbreviation): "
            ),
        }
    )

    print("=== User created successfully! ===")


def create_account(agency, account_number, users):
    cpf = input("Enter CPF user (number only): ")
    user = filter_user(cpf, users)

    if user:
        print("\n=== Account created successfully! ===")
        return {"agency": agency, "account_number": account_number, "usuario": user}

    print("\n@@@ User not found, account creation flow closed! @@@")


def list_accounts(accounts):
    for account in accounts:
        linha = f"""\
            Agency:\t{account["agency"]}
            Account:\t\t{account["account_number"]}
            Holder:\t{account["usuario"]["nome"]}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def menu():
    menu = """

    [d] Deposit
    [w] Withdraw
    [s] Statement
    [na] New Account
    [la] List Accounts
    [nu] New User
    [q] Quit

    => """

    return input(menu)


def main():
    AGENCY = "0001"
    MAX_WITHDRAWALS = 3

    balance = 0
    limit = 500
    statement = ""
    withdrawal_count = 0
    users = []
    accounts = []

    while True:
        option = menu()

        if option == "d":
            balance, statement = deposit(balance, statement)
            continue

        if option == "w":
            balance, statement, withdrawal_count = withdraw(
                balance, statement, withdrawal_count, limit, MAX_WITHDRAWALS
            )
            continue

        if option == "s":
            show_statement(balance, statement)
            continue

        if option == "nu":
            create_user(users)
            continue

        if option == "na":
            account_number = len(accounts) + 1
            conta = create_account(AGENCY, account_number, users)

            if conta:
                accounts.append(conta)
            continue

        if option == "la":
            list_accounts(accounts)
            continue

        if option == "q":
            break

        print("Invalid operation, please select a valid option.")


main()
