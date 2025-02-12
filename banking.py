# Description: A simple banking application that allows users to create accounts, deposit, withdraw, transfer money, check balance, view transaction history, save and load account data to/from a file.

import argparse

import json

class Bank:
    def __init__(self):
        self.accounts = {}
        self.transactions = {}

        # Function to create new bank account
    def create_account(self, account_id):
            #check if account exists
        if account_id in self.accounts:
            print(f"Error: Account {account_id} already exists.")
            return
            #check if account id is a positive integer
        if not isinstance(account_id, int) or account_id <= 0:
            print("Error: Account ID must be a positive integer.")
            return
            #create account with an empty history and balance of 0
        else:
            self.accounts[account_id] = 0
            self.transactions[account_id] = []
            print(f"Account {account_id} created successfully.")

        # Function to deposit money into an account
    def deposit(self, account_id, amount):
                #check if amount is positive
            if amount <= 0:
                print("Error: Deposit amount must be positive.")
                return
                #check if account exists
            if account_id not in self.accounts:
                print(f"Error: Account {account_id} does not exist.")
                return
                #deposit money into account, update transaction history for account, then print new balance with 2 decimal figures
            self.accounts[account_id] = round(self.accounts[account_id] + amount, 2)
            self.transactions[account_id].append(f"Deposited {amount:.2f}")
            print(f"Deposited {amount:.2f} to account {account_id}. New balance: {self.accounts[account_id]:.2f}")

        # Function to withdraw money from an account (similar comment logic as deposit function)
    def withdraw(self, account_id, amount):

            if amount <= 0:
                print("Error: Withdrawal amount must be positive.")
                return
            if account_id not in self.accounts:
                print(f"Error: Account {account_id} does not exist.")
                return
            if self.accounts[account_id] < amount:
                print("Error: Insufficient funds.")
                return
            self.accounts[account_id] = round(self.accounts[account_id] - amount, 2)
            self.transactions[account_id].append(f"Withdrew {amount:.2f}")
            print(f"Withdrew {amount:.2f} from account {account_id}. New balance: {self.accounts[account_id]:.2f}")

        # Function to check account balance
    def check_balance(self, account_id):
        if account_id not in self.accounts:
            print(f"Error: Account {account_id} does not exist.")
            return
        print(f"Account {account_id} balance: {self.accounts[account_id]:.2f}")

        # Function to transfer money between accounts, again similar logic other than transaction history
    def transfer(self, from_account, to_account, amount):

            if amount <= 0:
                print("Error: Transfer amount must be positive.")
                return
            if from_account not in self.accounts:
                print(f"Error: Account {from_account} does not exist.")
                return
            if to_account not in self.accounts:
                print(f"Error: Account {to_account} does not exist.")
                return
            if self.accounts[from_account] < amount:
                print("Error: Insufficient funds.")
                return
            
                #money transfer completed, transaction history is updated for both users, accessible in both their account histories
            self.accounts[from_account] -= amount
            self.accounts[to_account] += amount
            self.transactions[from_account].append(f"Transferred {amount:.2f} to {to_account}")
            self.transactions[to_account].append(f"Received {amount:.2f} from {from_account}")
            print(f"Transferred {amount:.2f} from {from_account} to {to_account}.")

        #function to show transaction history for account, then show current balance
    def transaction_history(self, account_id):
        if account_id not in self.transactions:
            print(f"Error: Account {account_id} does not exist.")
            return
        print(f"Transaction history for account {account_id}:")
        for transaction in self.transactions[account_id]:
            print(transaction)
        print(f"Current balance: {self.accounts[account_id]:.2f}")

        #function to save current memory to json file
    def save_to_file(self, filename):
        try:
            with open(filename, 'w') as file:
                    #creating json file with 2 objects, accounts and transactions. Using indent 2 for some readibility but with less overall space taken up
                json.dump({'accounts': self.accounts, 'transactions': self.transactions}, file, indent=2)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")

        #function to load data from json file
    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                    #updates current accounts from values in file, rounding to 2 decimal places 
                self.accounts = {key: round(value, 2) for key, value in data.get('accounts', {}).items()}
                self.transactions = data.get('transactions', {})
            print(f"Data loaded from {filename}")
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
        except Exception as e:
            print(f"Error loading data: {e}")

    #function to handle all transactions, using argparse to parse input
def handle_transaction(bank, parsed_args):
        if parsed_args.create_account:
            bank.create_account(parsed_args.create_account)
        elif parsed_args.deposit:
            bank.deposit(parsed_args.deposit[0], float(parsed_args.deposit[1]))
        elif parsed_args.withdraw:
            bank.withdraw(parsed_args.withdraw[0], float(parsed_args.withdraw[1]))
        elif parsed_args.balance:
            bank.check_balance(parsed_args.balance)
        elif parsed_args.transfer:
            bank.transfer(parsed_args.transfer[0], parsed_args.transfer[1], float(parsed_args.transfer[2]))
        elif parsed_args.history:
            bank.transaction_history(parsed_args.history)
        elif parsed_args.save_file:
            bank.save_to_file(parsed_args.save_file)
        elif parsed_args.load_file:
            bank.load_from_file(parsed_args.load_file)

    #main function to run the program
def main():
    print("Welcome to Perforce Banking")
    bank = Bank()
    parser = argparse.ArgumentParser(description="Bank CLI")
    parser.add_argument("--exit", action="store_true", help="Exit the program")
    parser.add_argument("--create-account", type=str, help="Create a new bank account")
    parser.add_argument("--deposit", nargs=2, metavar=("accountID", "amount"), help="Deposit money")
    parser.add_argument("--withdraw", nargs=2, metavar=("accountID", "amount"), help="Withdraw money")
    parser.add_argument("--balance", type=str, help="Check account balance")
    parser.add_argument("--transfer", nargs=3, metavar=("fromAccountID", "toAccountID", "amount"), help="Transfer money")
    parser.add_argument("--history", type=str, help="View transaction history")
    parser.add_argument("--save-file", type=str, help="Save all account data to a file")
    parser.add_argument("--load-file", type=str, help="Load account data from a file")
    while True:
        user_input = input("enter command-> ").strip().split()
        if not user_input:
            continue
        try:
            parsed_args = parser.parse_args(user_input)
            if parsed_args.exit:
                print("Exiting program.")
                break
            else:
                handle_transaction(bank, parsed_args)
            #stopping the program from exitting if an error is thrown by argparse (eg, invalid input etc.)
        except SystemExit:
            pass
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()