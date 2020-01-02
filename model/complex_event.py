from model.database import Base


class ComplexEvent(Base):
    @classmethod
    def select_all_from_parent_query(cls, *args):
        complex_name = args[0]

        return f'SELECT Event.type, Event.title, Event.text, ComplexEvent.from_date, ComplexEvent.to_date' \
               f' FROM ComplexEvent ' \
               f'INNER JOIN Event ON ComplexEvent.event_id = Event.id ' \
               f'INNER JOIN Complex ON Event.complex_id = Complex.id' \
               f'WHERE Complex.name="{complex_name}";'

    @classmethod
    def select_all_query(cls):
        return 'SELECT * FROM ComplexEvent;'

    @classmethod
    def select_one_query(cls, *args):
        event_type = args[0]
        event_title = args[1]
        event_from_date = args[2]
        event_to_date = args[3]
        complex_name = args[4]

        employee_id = cls.select_parent(1, complex_name)

        return f'SELECT * FROM ComplexEvent ' \
            f'WHERE ComplexEvent.type={event_type} AND ComplexEvent.title="{event_title}" AND ComplexEvent.from_date="{event_from_date}" ' \
            f'AND ComplexEvent.to_date="{event_to_date}" AND ComplexEvent.employee_id={employee_id};'

    @classmethod
    def insert_query(cls, *args):
        event_type = args[0]
        event_title = args[1]
        event_text = args[2]
        event_from_date = args[3]
        event_to_date = args[4]
        complex_name = args[3]

        complex_id = cls.select_parent(complex_name)
        if not complex_id:
            complex_id = cls.insert_parent(complex_name)

        return f'INSERT INTO ComplexEvent (type, title, text, from_date, to_date, complex_id) ' \
            f'VALUES ({event_type}, "{event_title}", "{event_text}", "{event_from_date}", "{event_to_date}", {complex_id});'

    @classmethod
    def delete_query(cls, *args):
        event_type = args[0]
        event_title = args[1]
        event_from_date = args[3]
        event_to_date = args[4]
        complex_name = args[3]

        complex_id = cls.select_parent(complex_name) or -1
            
        return f'DELETE FROM ComplexEvent ' \
            f'WHERE ComplexEvent.type={event_type} AND ComplexEvent.title="{event_title}" AND ComplexEvent.text="{event_text}" AND ComplexEvent.from_date="{event_from_date}" ' \
            f'AND ComplexEvent.to_date="{event_to_date}" AND ComplexEvent.complex_id={complex_id};'

    @classmethod
    def select_parent_query(cls, *args):
        complex_name = args[0]
        return f'SELECT id FROM Complex WHERE Complex.name="{complex_name}";'

    @classmethod
    def insert_parent_query(cls, *args):
        complex_name = args[0]
        return f'INSERT INTO Complex (name) VALUES ("{complex_name}");'
