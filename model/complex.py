from model.database import Base


class Complex(Base):
    @classmethod
    def select_all_from_parent_query(cls, *args):
        return 'SELECT * FROM Complex;'

    @classmethod
    def insert_query(cls, *args):
        name = args[0]
        return f'INSERT INTO COMPLEX (name) VALUES ("{name}")'

    @classmethod
    def delete_query(cls, *args):
        name = args[0]
        return f'DELETE FROM Complex WHERE Complex.name="{name}";'
