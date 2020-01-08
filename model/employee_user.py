from model.database import Base


class EmployeeUser(Base):
    @classmethod
    def select_one_query(cls, *args):
        username = args[0]

        return f'SELECT * FROM EmployeeUser WHERE EmployeeUser.username="{username}";'

    @classmethod
    def insert_query(cls, *args):
        cpf = args[0]
        password = args[1]
        name = args[2]
        age = args[3]
        role = args[4]
        complex_name = args[5]

        employee_id = cls.select_parent(0, cpf, role, complex_name)
        if not employee_id:
            employee_id = cls.insert_parent(0, cpf, name, age, role, complex_name)

        return f'INSERT INTO EmployeeUser (username, password, employee_id) VALUES ("{cpf}", "{password}", {employee_id});'

    @classmethod
    def delete_query(cls, *args):
        cpf = args[0]
        role = args[3]
        complex_name = args[4]

        employee_id = cls.select_parent(0, cpf, role, complex_name)

        return f'DELETE FROM EmployeeUser WHERE EmployeeUser.username="{cpf}" AND EmployeeUser.employee_id={employee_id};'

    @classmethod
    def select_parent_query(cls, *args):
        parent_number = args[0]
        if parent_number == 0:
            cpf = args[1]
            role = args[2]
            complex_name = args[3]

            complex_id = cls.select_parent(1, complex_name)

            return f'SELECT id FROM Employee WHERE Employee.cpf="{cpf}" AND Employee.role="{role}" AND Employee.complex_id={complex_id};'

        elif parent_number == 1:
            complex_name = args[1]
            return f'SELECT id FROM Complex WHERE Complex.name="{complex_name}";'

    @classmethod
    def insert_parent_query(cls, *args):
        parent_number = args[0]
        if parent_number == 0:
            cpf = args[1]
            name = args[2]
            age = args[3]
            role = args[4]
            complex_name = args[5]

            complex_id = cls.select_parent(1, complex_name)
            if not complex_id:
                complex_id = cls.insert_parent(1, complex_name)

            return f'INSERT INTO Employee (cpf, name, age, role, complex_id) VALUES ("{cpf}", "{name}", {age}, "{role}", {complex_id});'

        elif parent_number == 1:
            complex_name = args[1]
            return f'INSERT INTO Complex (name) VALUES ("{complex_name}");'
