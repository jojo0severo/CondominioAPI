from model.database import Base


class Tower(Base):
    @classmethod
    def select_all_query(cls):
        return 'SELECT * FROM Tower;'

    @classmethod
    def select_one_query(cls, *args):
        tower_id = args[0]
        bloc_id = args[1]
        return f'SELECT * FROM Tower WHERE Tower.id="{tower_id}" AND Tower.bloc_id="{bloc_id}";'

    @classmethod
    def insert_query(cls, *args):
        tower_id = args[0]
        complex_name = args[1]

        complex_id = cls.select_parent(complex_name)
        if not complex_id:
            complex_id = cls.insert_parent(complex_name)

        return f'INSERT INTO Tower (id, complex_id) VALUES ("{tower_id}", {complex_id});'

    @classmethod
    def delete_query(cls, *args):
        tower_id = args[0]
        complex_name = args[1]

        complex_id = cls.select_parent(complex_name) or -1

        return f'DELETE FROM Tower WHERE Tower.id="{tower_id}" AND Tower.complex_id={complex_id};'

    @classmethod
    def select_parent_query(cls, *args):
        complex_name = args[0]

        return f'SELECT id FROM Complex WHERE Complex.name="{complex_name}";'

    @classmethod
    def insert_parent_query(cls, *args):
        complex_name = args[0]
        return f'INSERT INTO Complex (name) VALUES ("{complex_name}");'

