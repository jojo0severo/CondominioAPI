from model.database import Base


class Rule(Base):
    @classmethod
    def select_all_from_parent_query(cls, *args):
        complex_name = args[0]
        complex_id = cls.select_parent(complex_name)

        return f'SELECT * FROM Rule WHERE Rule.complex_id={complex_id};'

    @classmethod
    def select_one_query(cls, *args):
        rule_text = args[0]
        complex_name = args[2]

        complex_id = cls.select_parent(complex_name)

        return f'SELECT * FROM Rule WHERE Rule.text="{rule_text}" AND Rule.complex_id={complex_id};'

    @classmethod
    def insert_query(cls, *args):
        rule_text = args[0]
        complex_name = args[1]

        complex_id = cls.select_parent(complex_name)
        if not complex_id:
            complex_id = cls.insert_parent(complex_name)

        return f'INSERT INTO Rule (text, complex_id) VALUES ("{rule_text}", {complex_id});'

    @classmethod
    def delete_query(cls, *args):
        rule_text = args[0]
        complex_name = args[1]

        complex_id = cls.select_parent(complex_name)

        return f'DELETE FROM Rule WHERE AND Rule.text="{rule_text}" AND Rule.complex_id={complex_id};'

    @classmethod
    def select_parent_query(cls, *args):
        complex_name = args[0]
        return f'SELECT id FROM Complex WHERE Complex.name="{complex_name}";'

    @classmethod
    def insert_parent_query(cls, *args):
        complex_name = args[0]
        return f'INSERT INTO Complex (name) VALUES ("{complex_name}");'

