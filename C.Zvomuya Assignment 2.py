# Encapsulation - A Bank Account that protects its balance.

class BankAccount:
    def __init__(self, account_holder, opening_balance=0.0):
        self.account_holder = account_holder  # public attribute
        self.__balance = 0.0  # PRIVATE attribute (name mangled)
        if opening_balance > 0:
            self.__balance = float(opening_balance)

    def deposit(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be numeric.")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.__balance += amount
        return self.__balance

    def withdraw(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be numeric.")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.__balance:
            raise ValueError("Insufficient funds.")
        self.__balance -= amount
        return self.__balance

    def display_balance(self):
        print(f"Account holder : {self.account_holder}")
        print(f"Current balance: ${self.__balance:,.2f}")


@property
def balance(self):
    """Read-only view of the balance - there is no setter."""
    return self.__balance


if __name__ == "__main__":
    account = BankAccount("Benigna Chikava", 500)
    account.display_balance()

    account.deposit(250.50)
    account.withdraw(100)
    account.display_balance()

print("\n1. Trying to assign to the read-only property:")
try:
    account.balance = 1_000_000
except AttributeError as error:
    print("   Blocked ->", error)

print("2. Trying to reach the private attribute by name:")
try:
    print(account.__balance)
except AttributeError as error:
    print("   Blocked ->", error)

print("3. Trying an invalid withdrawal:")
try:
    account.withdraw(999_999)
except ValueError as error:
    print("   Blocked ->", error)

print("4. Assigning `account.__balance = 0` creates a NEW, unrelated attribute:")
account.__balance = 0
print(f"   Real balance is still ${account.balance:,.2f}")
print(f"   Name-mangled to: {account._BankAccount__balance:,.2f}")


        ##Question 1: Connect to SQLite, create a table, insert data, retrieve data.

import sqlite3


def main():
    # 1. Connect (the file is created automatically if it does not exist)
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    try: 2. Create the table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                name    TEXT    NOT NULL,
                course  TEXT    NOT NULL,
                mark    REAL
            )
        """)

        # 3. Insert data (parameterised - never use string formatting)
        cursor.execute("DELETE FROM students")  # keep re-runs clean
        cursor.execute(
            "INSERT INTO students (name, course, mark) VALUES (?, ?, ?)",
            ("Tinashe Moyo", "Python Programming", 72.5),
        )
        cursor.executemany(
            "INSERT INTO students (name, course, mark) VALUES (?, ?, ?)",
            [
                ("Rudo Chikwanha", "Database Systems", 65.0),
                ("Farai Ncube", "Python Programming", 81.0),
                ("Anesu Dube", "Networks", 58.5),
            ],
        )
        connection.commit()

        # 4. Retrieve the data
        cursor.execute("SELECT id, name, course, mark FROM students ORDER BY mark DESC")
        rows = cursor.fetchall()

        print(f"{'ID':<4}{'Name':<18}{'Course':<22}{'Mark':>6}")
        print("-" * 50)
        for row in rows:
            print(f"{row[0]:<4}{row[1]:<18}{row[2]:<22}{row[3]:>6.1f}")
        print(f"\n{len(rows)} record(s) retrieved.")

    except sqlite3.Error as error:
        print("Database error:", error)

    finally:
        # 5. Always close the connection
        connection.close()


if __name__ == "__main__":
    main()

# Question 3 (server): listens on localhost:65432 and prints what it receives.

"""
Question 3 (server): Socket listens on localhost:65432 and prints what it receives.
"""
import socket

HOST = "127.0.0.1"
PORT = 65432

def main():
    try:
        # AF_INET = IPv4, SOCK_STREAM = TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Allow reuse of the port immediately after the server stops
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            print(f"Server listening on {HOST}:{PORT}")

            connection, address = server_socket.accept()
            with connection:
                print(f"Connected by {address}")
                data = connection.recv(1024)
                if data:
                    message = data.decode("utf-8")
                    print(f"Received: {message}")
                    connection.sendall(b"Message received. Thank you!")
                else:
                    print("Client connected but sent no data.")
    except OSError as error:
        print("Socket error:", error)
    except KeyboardInterrupt:
        print("\nServer shut down by user.")

if __name__ == "__main__":
    main()

# Question 3 (client): Connects to the server and sends a greeting.

import socket

HOST = "127.0.0.1"
PORT = 65432

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            message = "Hello, Server!"
            client_socket.sendall(message.encode("utf-8"))
            data = client_socket.recv(1024)
            print("Server reply:", data.decode("utf-8"))
    except socket.timeout:
        print("Connection timed out — server unresponsive.")
    except socket.gaierror:
        print("Hostname could not be resolved.")
    except OSError as error:
        print("Socket error:", error)

if __name__ == "__main__":
    main()

# Question 4: 5 random floats between 0 and 10, then min and max.

import random


def main():
    # random.uniform(a, b) returns a float in the range [a, b]
    numbers = [random.uniform(0, 10) for _ in range(5)]

    print("Generated numbers:")
    for index, value in enumerate(numbers, start=1):
        print(f"  {index}. {value:.4f}")

    print(f"\nMinimum value: {min(numbers):.4f}")
    print(f"Maximum value: {max(numbers):.4f}")


if __name__ == "__main__":
    main()

# Question 5: An abstract FileHandler with concrete Text and Binary subclasses.

from abc import ABC, abstractmethod


class FileHandler(ABC):
    """Contract that every file handler must honour."""

    def __init__(self, filename):
        self.filename = filename

    @abstractmethod
    def read(self):
        """Return the contents of the file."""

    @abstractmethod
    def write(self, data):
        """Write data to the file."""

    # A concrete method - shared by every subclass, no need to re-implement
    def describe(self):
        return f"{self.__class__.__name__} managing '{self.filename}'"


class TextFileHandler(FileHandler):
    """Reads and writes UTF-8 text."""

    def read(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            return file.read()

    def write(self, data):
        with open(self.filename, "w", encoding="utf-8") as file:
            file.write(data)


class BinaryFileHandler(FileHandler):
    """Reads and writes raw bytes."""

    def read(self):
        with open(self.filename, "rb") as file:
            return file.read()

    def write(self, data):
        with open(self.filename, "wb") as file:
            file.write(data)


if __name__ == "__main__":
    text_handler = TextFileHandler("notes.txt")
    text_handler.write("Encapsulation, inheritance, polymorphism, abstraction.")
    print(text_handler.describe())
    print("Read back:", text_handler.read())

    binary_handler = BinaryFileHandler("data.bin")
    binary_handler.write(b"\x50\x59\x54\x48\x4f\x4e")
    print(binary_handler.describe())
    print("Read back:", binary_handler.read())

    # Polymorphism: the loop does not care which subclass it is holding
    print("\nPolymorphic loop:")
    for handler in (text_handler, binary_handler):
        print(" ", handler.describe(), "->", len(handler.read()), "units read")

    # Proof that the abstract class cannot be instantiated
    print("\nTrying to instantiate FileHandler directly:")
    try:
        FileHandler("anything.txt")
    except TypeError as error:
        print("  Blocked ->", error)

# Question 6: Vehicle base class with Car and Bike subclasses overriding a method.

class Vehicle:
    """Base class holding what every vehicle has in common."""

    def __init__(self, make, model, wheels=4):
        self.make = make
        self.model = model
        self.wheels = wheels

    def describe(self):
        return f"{self.make} {self.model} with {self.wheels} wheel(s)"

    # This is the method the subclasses will override
    def start_engine(self):
        return "The vehicle starts."


class Car(Vehicle):
    def __init__(self, make, model, doors=4):
        super().__init__(make, model, wheels=4)  # reuse the base constructor
        self.doors = doors

    def start_engine(self):  # OVERRIDE
        return f"The {self.make} {self.model} starts with the push of a button. Vroom!"

    def describe(self):  # OVERRIDE that extends the base
        return super().describe() + f" and {self.doors} doors"


class Bike(Vehicle):
    def __init__(self, make, model, engine_cc=150):
        super().__init__(make, model, wheels=2)
        self.engine_cc = engine_cc

    def start_engine(self):  # OVERRIDE
        return f"The {self.make} {self.model} ({self.engine_cc}cc) kick-starts. Brrrm!"


if __name__ == "__main__":
    vehicles = [
        Vehicle("Generic", "Transport"),
        Car("Toyota", "Corolla", doors=4),
        Bike("Honda", "CG125", engine_cc=125),
    ]

    for vehicle in vehicles:
        print(vehicle.describe())
        print("  ", vehicle.start_engine())  # polymorphism in action
        print()

    car = vehicles[1]
    print("isinstance(car, Vehicle):", isinstance(car, Vehicle))
    print("Base version, called explicitly:", Vehicle.start_engine(car))









