"""
==============================================================
07 - OOP BASICS: Classes, __init__, self, methods
==============================================================

CONCEPT:
- `class ClassName:` to define
- `__init__` is the constructor (like `constructor()` in TS)
- `self` refers to the instance (like `this` in JS)
- Must pass `self` as the first parameter of instance methods
"""

# ---------------- EXAMPLE 1: Simple class ----------------
print("=== Example 1: Simple Class ===")

class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Hi, I'm {self.name}, age {self.age}"

    def have_birthday(self) -> None:
        self.age += 1
        print(f"{self.name} is now {self.age}")


p1 = Person("Mutyala", 30)
p2 = Person("Alice", 25)

print(p1.greet())
print(p2.greet())
p1.have_birthday()


# ---------------- EXAMPLE 2: Bank Account (real world) ----------------
print("\n=== Example 2: Bank Account ===")

class BankAccount:
    # Class variable (shared across instances)
    bank_name = "Python Bank"

    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self.balance = balance          # instance variable
        self._transactions = []          # "_" = convention for private

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount
        self._transactions.append(f"Deposit: +{amount}")
        print(f"Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        self._transactions.append(f"Withdraw: -{amount}")
        print(f"Withdrew {amount}. New balance: {self.balance}")

    def show_history(self) -> None:
        print(f"--- {self.owner}'s transactions ---")
        for t in self._transactions:
            print(f"  {t}")


acc = BankAccount("Mutyala", 1000)
acc.deposit(500)
acc.withdraw(200)
acc.deposit(100)
acc.show_history()
print(f"Final balance: {acc.balance}")
print(f"Bank: {BankAccount.bank_name}")


# ---------------- TRY IT YOURSELF ----------------
# 1. Create a `Car` class with make, model, year, and a `describe()` method
# 2. Add a `Rectangle` class with width/height, methods: area(), perimeter()
# 3. Create a `ToDoList` class with add_task, remove_task, show_tasks methods
