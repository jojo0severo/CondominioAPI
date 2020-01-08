from model.database import Base


class Employee(Base):
    @classmethod
    def select_all_from_parent_query(cls, *args):
        complex_name = args[0]
        complex_id = cls.select_parent(1, complex_name)

        return f'SELECT * FROM Employee WHERE Employee.complex_id={complex_id};'

    @classmethod
    def select_one_query(cls, *args):
        cpf = args[0]
        name = args[1]
        age = args[2]
        role = args[3]
        complex_name = args[4]

        complex_id = cls.select_parent(complex_name)

        return f'SELECT * FROM Employee ' \
            f'WHERE Employee.cpf="{cpf}" AND Employee.role="{role}" AND Employee.name="{name}" ' \
            f'AND Employee.age={age} AND Employee.complex_id={complex_id};'

    @classmethod
    def insert_query(cls, *args):
        cpf = args[0]
        name = args[1]
        age = args[2]
        role = args[3]
        complex_name = args[4]

        complex_id = cls.select_parent(complex_name)
        if not complex_id:
            complex_id = cls.insert_parent(complex_name)

        return f'INSERT INTO Employee (cpf, role, name, age, complex_id) VALUES ("{cpf}", "{role}", "{name}", {age}, {complex_id});'

    @classmethod
    def delete_query(cls, *args):
        cpf = args[0]
        name = args[1]
        age = args[2]
        role = args[3]
        complex_name = args[4]

        complex_id = cls.select_parent(complex_name)

        return f'DELETE FROM Employee ' \
            f'WHERE Employee.cpf="{cpf}" AND Employee.role="{role}" AND Employee.name="{name}" AND Employee.age={age} AND Employee.complex_id={complex_id};'

    @classmethod
    def select_parent_query(cls, *args):
        complex_name = args[0]
        return f'SELECT id FROM Complex WHERE Complex.name="{complex_name}";'

    @classmethod
    def insert_parent_query(cls, *args):
        complex_name = args[0]
        return f'INSERT INTO Complex (name) VALUES ("{complex_name}");'
