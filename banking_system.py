menu = """

[d] Deposit
[w] Withdraw
[s] Statement
[q] Quit

=> """

balance = 0
limit = 500
statement = ""
withdrawal_count = 0
MAX_WITHDRAWALS = 3

while True:
    option = input(menu)

    if option == "d":
        amount = float(input("Enter the deposit amount: "))

        if amount <= 0:
            print("Operation failed! The entered amount is invalid.")
            continue

        balance += amount
        statement += f"Deposit: $ {amount:.2f}\n"
        continue

    if option == "w":
        amount = float(input("Enter the withdrawal amount: "))

        if amount <= 0:
            print("Operation failed! The entered amount is invalid.")
            continue

        if amount > balance:
            print("Operation failed! Insufficient balance.")
            continue

        if amount > limit:
            print("Operation failed! The withdrawal amount exceeds the limit.")
            continue

        if withdrawal_count >= MAX_WITHDRAWALS:
            print("Operation failed! Maximum number of withdrawals exceeded.")
            continue

        balance -= amount
        statement += f"Withdrawal: $ {amount:.2f}\n"
        withdrawal_count += 1
        continue

    if option == "s":
        print("\n========== STATEMENT ==========")
        print("No transactions have been made." if not statement else statement)
        print(f"\nBalance: $ {balance:.2f}")
        print("================================")
        continue

    if option == "q":
        break

    print("Invalid operation, please select a valid option.")
