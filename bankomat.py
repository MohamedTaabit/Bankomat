import json
import os
from datetime import datetime
from colorama import init, Fore, Style

# Automatically reset terminal color after each print.
init(autoreset=True)

accounts = {}


def load_accounts():
    """ Ladda konton från JSON-filen. Om filen inte finns returneras en tom ordbok."""
    if not os.path.exists("accounts.json"):
        return {}

    with open("accounts.json", "r", encoding="utf-8") as file:
        data = file.read()
        if not data:
            return {}
        return json.loads(data)


def save_accounts():
    """Sparar konton till JSON-filen."""
    with open("accounts.json", "w", encoding="utf-8") as file:
        json.dump(accounts, file, indent=4)
        file.write("\n\n")


def create_account():
    """Skapa ett nytt konto med användarinmatat kontonummer."""
    while True:
        acc_num = input(Fore.BLUE + "\nAnge ett giltig kontonummer (Skriv 0 för att återgå till Huvudmeny): ")

        if acc_num.lower() == '0':
            return

        if not acc_num.isdigit():
            print(Fore.RED + "Kontonummer måste vara numeriskt.")
            continue

        if acc_num in accounts:
            print(Fore.RED + "Detta kontonummer är redan taget.")
            continue

        accounts[acc_num] = {'Balance': 0.0, 'Transactions': []}
        print(Fore.GREEN + f"Konto {acc_num} har skapats!")
        save_accounts()
        break


def manage_account():
    """Administrera ett befintligt konto genom att välja alternativ från en meny."""
    acc_num = input(Fore.BLUE + "\nAnge ett kontonummer: ")

    if acc_num not in accounts:
        print(Fore.RED + "Detta kontonummer finns inte.")
        return

    while True:
        print(Fore.CYAN + "\nKontomeny:")
        print("1. Ta ut pengar")
        print("2. Sätt in pengar")
        print("3. Visa saldo")
        print("4. Avsluta")

        choice = input(Fore.BLUE + "Välj ett alternativ: ")

        if choice == "1":
            amount_str = input("Ange belopp att ta ut: ")
            if not amount_str.replace(".", "").isdigit():
                print(Fore.RED + "Ange ett giltigt belopp.")
                continue

            amount = float(amount_str)
            if amount <= 0:
                print(Fore.RED + "Beloppet måste vara större än 0.")
                continue

            if amount > accounts[acc_num]['Balance']:
                print(Fore.RED + "Du har inte tillräckligt med pengar på kontot.")
                continue

            accounts[acc_num]['Balance'] -= amount
            date = datetime.now().strftime("%Y-%m-%d")
            accounts[acc_num]['Transactions'].append({"Type": "Withdraw", "Amount": -amount, "Date": date})
            print(Fore.GREEN + f"{amount} kr har tagits ut.")
            save_accounts()

        elif choice == "2":
            amount_str = input("Ange belopp att sätta in: ")
            if not amount_str.replace(".", "").isdigit():
                print(Fore.RED + "Ange ett giltigt belopp.")
                continue

            amount = float(amount_str)
            if amount <= 0:
                print(Fore.RED + "Beloppet måste vara större än 0.")
                continue

            accounts[acc_num]['Balance'] += amount
            date = datetime.now().strftime("%Y-%m-%d")
            accounts[acc_num]['Transactions'].append({"Type": "Deposit", "Amount": amount, "Date": date})
            print(Fore.GREEN + f"{amount} kr har satts in.")
            save_accounts()

        elif choice == "3":
            print(Fore.YELLOW + f"Ditt saldo är: {accounts[acc_num]['Balance']} kr")
            print("Transaktioner:")
            for trans in accounts[acc_num]['Transactions']:
                t_type = 'INSÄTTNING' if trans['Type'] == 'Deposit' else 'UTTAG'
                color = Fore.GREEN if t_type == 'INSÄTTNING' else Fore.RED
                print(f"{color}{t_type}: {trans['Amount']} kr, Datum: {trans['Date']}")

        elif choice == "4":
            break

        else:
            print(Fore.RED + "Ogiltigt val. Försök igen.")


def main():
    global accounts
    accounts = load_accounts()

    while True:
        print(Fore.CYAN + "\n***Huvudmeny***: ")
        print("1. Skapa konto")
        print("2. Administrera konto")
        print("3. Avsluta")
        choice = input(Fore.BLUE + "Välj ett alternativ: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            manage_account()
        elif choice == "3":
            print(Fore.GREEN + "Tack för att du använde bankomaten!")
            break
        else:
            print(Fore.RED + "Ogiltigt val. Försök igen.")


if __name__ == "__main__":
    main()
