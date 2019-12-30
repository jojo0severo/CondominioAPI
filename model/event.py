from model.database import Base


class Event(Base):
    @classmethod
    def __select_all_query(cls):
        return 'SELECT * FROM Event;'

    @classmethod
    def __select_one_query(cls, *args):
        complex_name = args[0]
        return f'SELECT * FROM Event WHERE Event.name={complex_name};'

    @classmethod
    def __insert_query(cls, *args):
        name = args[0]
        return f'INSERT INTO COMPLEX (name) VALUES ("{name}")'

    @classmethod
    def __delete_query(cls, *args):
        name = args[0]
        return f'DELETE FROM Complex WHERE Complex.name="{name}";'
