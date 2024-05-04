SQL_CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS costumer(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cpf TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL)
"""

SQL_INSERT = """
    INSERT INTO costumer(name, cpf, email, age)
    VALUES(?, ?, ?, ?)
"""

SQL_GET_ALL = """
    SELECT id, name, cpf, email, age
    FROM costumer
    ORDER BY name
"""

SQL_UPDATE = """
    UPDATE costumer
    SET name=?, cpf=?, email=?, age=?
    WHERE id=?
"""

SQL_DELETE = """
    DELETE FROM costumer
    WHERE id=?
"""
SQL_GET_ONE = """
    SELECT id, name, cpf, email, age
    FROM costumer
    WHERE id=?
"""
SQL_GET_COUNT = """"
    SELECT COUNT(*) FROM costumer
"""

SQL_GET_BY_CPF = """
    SELECT id FROM costumer
    WHERE cpf=?
"""
SQL_GET_BY_EMAIL = """
    SELECT id FROM costumer
    WHERE email=?
"""