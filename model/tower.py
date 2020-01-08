from model.database import Base


class Tower(Base):
    @classmethod
    def select_all_from_parent_query(cls, *args):
        complex_name = args[0]

        complex_id = cls.select_parent(complex_name)

        return f'SELECT * FROM Tower WHERE Tower.complex_id={complex_id};'

    @classmethod
    def select_one_query(cls, *args):
        tower_name = args[0]
        complex_name = args[1]

        complex_id = cls.select_parent(complex_name)

        return f'SELECT * FROM Tower WHERE Tower.name="{tower_name}" AND Tower.complex_id={complex_id};'

    @classmethod
    def insert_query(cls, *args):
        tower_name = args[0]
        complex_name = args[1]

        complex_id = cls.select_parent(complex_name)
        if not complex_id:
            complex_id = cls.insert_parent(complex_name)

        return f'INSERT INTO Tower (name, complex_id) VALUES ("{tower_name}", {complex_id});'

    @classmethod
    def delete_query(cls, *args):
        tower_name = args[0]
        complex_name = args[1]

        complex_id = cls.select_parent(complex_name)

        return f'DELETE FROM Tower WHERE Tower.name="{tower_name}" AND Tower.complex_id={complex_id};'

    @classmethod
    def select_parent_query(cls, *args):
        complex_name = args[0]

        return f'SELECT id FROM Complex WHERE Complex.name="{complex_name}";'

    @classmethod
    def insert_parent_query(cls, *args):
        complex_name = args[0]
        return f'INSERT INTO Complex (name) VALUES ("{complex_name}");'

