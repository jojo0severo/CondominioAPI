from model.database import Base


class Warning(Base):
    @classmethod
    def select_all_query(cls):
        return 'SELECT * FROM Warning;'

    @classmethod
    def select_one_query(cls, *args):
        warning_type = args[0]
        warning_text = args[1]
        complex_name = args[2]

        complex_id = cls.select_parent(complex_name)
        if not complex_id:
            complex_id = cls.insert_parent(complex_name)

        return f'SELECT * FROM Warning WHERE Warning.type={warning_type} AND Warning.text="{warning_text}" AND Warning.complex_id={complex_id};'

    @classmethod
    def insert_query(cls, *args):
        warning_type = args[0]
        warning_text = args[1]
        complex_name = args[2]

        complex_id = cls.select_parent(complex_name)
        if not complex_id:
            complex_id = cls.insert_parent(complex_name)

        return f'INSERT INTO Warning (type, text, complex_id) VALUES ({warning_type}, "{warning_text}", {complex_id});'

    @classmethod
    def delete_query(cls, *args):
        warning_type = args[0]
        warning_text = args[1]
        complex_name = args[2]

        complex_id = cls.select_parent(complex_name) or -1

        return f'DELETE FROM Warning WHERE Warning.type={warning_type} AND Warning.text="{warning_text}" AND Warning.complex_id={complex_id};'

    @classmethod
    def select_parent_query(cls, *args):
        complex_name = args[0]
        return f'SELECT id FROM Complex WHERE Complex.name="{complex_name}";'

    @classmethod
    def insert_parent_query(cls, *args):
        complex_name = args[0]
        return f'INSERT INTO Complex (name) VALUES ("{complex_name}");'
