import sqlite3
from typing import List, Optional
from models.costumer import Costumer
from sql.costumer import *
from util.database import create_connection

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


class CostumerRepo:
    @classmethod
    def create_table(cls) -> bool:
        try:
            with create_connection() as conn:
                cursor = conn.cursor() # a cursor object is used to execute sql commands
                cursor.execute(SQL_CREATE_TABLE)
                return True        
        except sqlite3.Error as ex:
            print(ex)
            return False
        
    @classmethod
    def insert(cls, costumer: Costumer) -> Optional[Costumer]:
        try:
            with create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(SQL_INSERT, (
                    costumer.name,
                    costumer.cpf.replace('.','').replace('-',''),
                    costumer.email,
                    costumer.age
                ))
                if cursor.rowcount > 0:
                    costumer.id = cursor.lastrowid
                    return costumer        
        except sqlite3.Error as ex:
            print(ex)
            return None
        
    @classmethod
    def get_all(cls) -> List[Costumer]:
        try:
            with create_connection() as conn:
                cursor = conn.cursor()
                tuples = cursor.execute(SQL_GET_ALL).fetchall()
                costumers = []
                for t in tuples:
                    costumer = Costumer(*t)
                    if costumer.cpf:  # Verifica se o CPF não é None ou vazio
                        costumer.cpf = validate_cpf(str(costumer.cpf))  # Converte para string antes de validar
                    costumers.append(costumer)
                return costumers
        except sqlite3.Error as ex:
            print(ex)
            return []



    @classmethod
    def update(cls, costumer: Costumer) -> bool:
        try:
            with create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(SQL_UPDATE, (
                    costumer.name,
                    costumer.cpf,
                    costumer.email,
                    costumer.age,
                    costumer.id
                )) 
                if cursor.rowcount > 0:  
                    return True        
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def delete(cls, id: int) -> bool:
        try:
            with create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(SQL_DELETE, (id,)) #virgula para ser uma tupla e nao so um parametro
                if cursor.rowcount > 0:  
                    return True        
        except sqlite3.Error as ex:
            print(ex)
            return False
        
    @classmethod
    def get_one(cls, id: int) -> Optional[Costumer]:
        try:
            with create_connection() as conn:
                cursor = conn.cursor() 
                cursor.execute(SQL_GET_ONE, (id, ))
                tuple = cursor.fetchone()
                if tuple:
                    costumer = Costumer(*tuple)
                    return costumer
                else:
                    return None 
        except sqlite3.Error as ex:
            print(ex)
            return None



    @classmethod
    def get_count(cls) -> Optional[int]:
        try:
            with create_connection() as conn:
                cursor = conn.cursor() 
                tuple = cursor.execute(SQL_GET_COUNT).fetchone() 
                amount = int(tuple[0])
                return amount   
        except sqlite3.Error as ex:
            print(ex)
            return False