from model.database import Base


class Warning(Base):
    @classmethod
    def select_all_from_parent_query(cls, *args):
        complex_name = args[0]
        complex_id = cls.select_parent(1, complex_name)
        return f'SELECT * FROM Warning INNER JOIN Tower ON Warning.tower_id=Tower.id WHERE Tower.complex_id={complex_id};'

    @classmethod
    def select_all_query(cls):
        return 'SELECT * FROM Warning;'

    @classmethod
    def select_one_query(cls, *args):
        warning_text = args[0]
        tower_name = args[1]
        complex_name = args[2]

        tower_id = cls.select_parent(0, tower_name, complex_name)

        return f'SELECT * FROM Warning WHERE Warning.text="{warning_text}" AND Warning.tower_id={tower_id};'

    @classmethod
    def insert_query(cls, *args):
        warning_type = args[0]
        warning_text = args[1]
        tower_name = args[2]
        complex_name = args[3]

        tower_id = cls.select_parent(0, tower_name, complex_name)
        if not tower_id:
            tower_id = cls.insert_parent(0, tower_name, complex_name)

        return f'INSERT INTO Warning (type, text, tower_id) VALUES ({warning_type}, "{warning_text}", {tower_id});'

    @classmethod
    def delete_query(cls, *args):
        warning_text = args[0]
        tower_name = args[1]
        complex_name = args[2]

        tower_id = cls.select_parent(0, tower_name, complex_name)

        return f'DELETE FROM Warning WHERE Warning.text="{warning_text}" AND Warning.tower_id={tower_id};'

    @classmethod
    def select_parent_query(cls, *args):
        parent_number = args[0]
        if parent_number == 0:
            tower_name = args[1]
            complex_name = args[2]

            complex_id = cls.select_parent(1, complex_name)

            return f'SELECT id FROM Tower WHERE Tower.name="{tower_name}" AND Tower.complex_id={complex_id};'

        elif parent_number == 1:
            complex_name = args[1]

            return f'SELECT id FROM Complex WHERE Complex.name="{complex_name}";'

        else:
            raise RuntimeError(f'Internal error on warning parent selection. Arguments: {args}.')

    @classmethod
    def insert_parent_query(cls, *args):
        parent_number = args[0]
        if parent_number == 0:
            tower_name = args[1]
            complex_name = args[2]

            complex_id = cls.select_parent(1, complex_name)
            if not complex_id:
                complex_id = cls.insert_parent(1, complex_name)

            return f'INSERT INTO Tower (name, complex_id) VALUES ("{tower_name}", {complex_id});'

        elif parent_number == 1:
            complex_name = args[1]

            return f'INSERT INTO Complex (name) VALUES ("{complex_name}");'

        else:
            raise RuntimeError(f'Internal error on warning parent selection. Arguments: {args}.')
