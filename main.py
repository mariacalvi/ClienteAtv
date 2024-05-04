import os
import sqlite3
from typing import Optional
from models.costumer import Costumer
from sql.costumer import SQL_GET_BY_CPF, SQL_GET_BY_EMAIL
from util.database import create_connection
from repo.costumer import CostumerRepo, cpf_exists


CostumerRepo.create_table() 

def validate_cpf(cpf: str) -> Optional[str]:
    cpf_digits = [digit for digit in cpf if digit.isdigit()]
    if len(cpf_digits) == 11:
        cpf_formatado = f"{cpf_digits[0:3]}.{cpf_digits[3:6]}.{cpf_digits[6:9]}-{cpf_digits[9:]}"
        return cpf_formatado
    else:
        return None

def cpf_exists(cpf: str) -> bool:
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_GET_BY_CPF, (cpf,))
            existing_customer = cursor.fetchone()
            if existing_customer:
                return True
            else:
                return False
    except sqlite3.Error as ex:
        print(ex)
        return False
    
def email_exists(email: str) -> bool:
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_GET_BY_EMAIL, (email,))
            existing_costumer = cursor.fetchone()
            if existing_costumer:
                return True
            else:
                return False
    except sqlite3.Error as ex:
        print(ex)
        return False
 
def insert_costumer():
    print("Inserting Costumer")
    print("------------------")
    name = input("Name: ")

    if name.replace(" ", "").isalpha():
        cpf = input("CPF (format: xxx.xxx.xxx-xx): ")

        if len(cpf) == 14 and cpf[3] == '.' and cpf[7] == '.' and cpf[11] == '-':
            cpf_formatted = validate_cpf(cpf)
            if cpf_formatted:
                email = input("Email: ")
                if len(email) <= 256:
                    age_str = input("Age: ")
                    if age_str.isdigit():
                        age = int(age_str)
                        if 0 < age < 100:
                            if name and cpf_formatted and email:
                                if not cpf_exists(cpf_formatted):
                                    if not email_exists(email):
                                        costumer = Costumer(None, name, cpf_formatted, email, age)
                                        inserted_costumer = CostumerRepo.insert(costumer)
                                        if inserted_costumer:
                                            print("Costumer successfully inserted!")
                                        else:
                                            print("Failed to insert costumer.")
                                    else:
                                        print("Invalid email! This email is already registered.")
                                else:
                                    print("Invalid CPF! This CPF already exists in the database.")
                            else:
                                print("All fields are mandatory. Please fill in all required fields.")
                        else:
                            print("Invalid age! Age must be between 1 and 99.")
                    else:
                        print("Invalid age! Age must be a number.")
                else:
                    print("Invalid email! Email must have a maximum of 256 characters.")
            else:
                print("Invalid CPF format! CPF must be in the format xxx.xxx.xxx-xx.")
        else:
            print("Invalid CPF format! CPF must be in the format xxx.xxx.xxx-xx.")
    else:
        print("Invalid name! Name must contain only letters and spaces.")

def list_costumers():
    print("Listing costumers")
    print("----------------")
    print("ID|NAME")
    costumers = CostumerRepo.get_all()
    for p in costumers:
        print(f"{p.id:02d}|{p.name}")

def update_costumer():
    print("Updating costumer")
    print("------------------")
    id = int(input("Costumer Id: "))
    original_costumer = CostumerRepo.get_one(id)

    if original_costumer:
        new_name = input(f"New name ({original_costumer.name}):")
        new_cpf = input(f"New CPF ({original_costumer.cpf}):")
        new_email = input(f"New email ({original_costumer.email}):")
        new_age = input(f"New age: ({original_costumer.age}):")

        update_costumer = Costumer(id, new_name, new_cpf, new_email, new_age)
        if CostumerRepo.update(update_costumer):
            print("Costumer updated successfully!")
        else:
            print("Failed to update costumer.")
    else:
        print(f"No costumer found with ID {id}")


def delete_costumer():
    print("Deleting Costumer")
    print("------------------")
    id = int(input("Costumer ID: "))
    costumer = CostumerRepo.get_one(id)
    if costumer:
        answer = input(f"Are you sure to delete the costumer '{costumer.name}'?(Y/N)")
        if answer.upper() == "Y":
            if CostumerRepo.delete(id):
                print("Costumer deleted successfully!")
            else:
                print("Failed to delete costumer.")
    else:
        print(f"No costumer found with ID {id}")


def show_costumer():
    print("Showing Costumer")
    print("----------------")
    id = int(input("Costumer ID: "))
    costumer = CostumerRepo.get_one(id)

    if costumer:
        print(f"Name: {costumer.name}")
        print(f"CPF: {costumer.cpf}")
        print(f"Email: {costumer.email}")
        print(f"Age: {costumer.age}")
    else:
        print(f"No costumer found with ID {id}")

def show_menu():
    print("Costumers System")
    print("------------------------------")
    print("1. Insert Costumer")
    print("2. List Costumers")
    print("3. Update Costumer")
    print("4. Delete Costumer")
    print("5. Show Costumer")
    print("6. Exit")

def get_user_option() -> int:
    while True:
        try:
            option = int(input("Desired Option: "))
            return option
        except ValueError:
            print("Invalid input! Please enter a valid option.")

def clear_screen():
    os.system("cls") 

def wait_return_key():
    print("----------------------")
    print("Press RETURN to continue...")
    input()

while True:
    clear_screen()
    show_menu()
    option = get_user_option()
    clear_screen()
    match(option):
        case 1: insert_costumer()
        case 2: list_costumers()
        case 3: update_costumer()
        case 4: delete_costumer()
        case 5: show_costumer()
        case 6: break
        case _: print("Invalid option!")
    wait_return_key()

print("Thanks for using this program!!!")
