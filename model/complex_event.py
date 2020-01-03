from model.database import Base


class ComplexEvent(Base):
    @classmethod
    def select_all_from_parent_query(cls, *args):
        complex_name = args[0]

        return f'SELECT Event.type, Event.title, Event.text, ComplexEvent.from_date, ComplexEvent.to_date ' \
               f'FROM ComplexEvent ' \
               f'INNER JOIN Event ON ComplexEvent.event_id = Event.id ' \
               f'INNER JOIN Complex ON Event.complex_id = Complex.id ' \
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

        event_id = cls.select_parent(0, event_type, event_title, complex_name)

        return f'SELECT * FROM ComplexEvent ' \
            f'WHERE ComplexEvent.event_id={event_id} AND ComplexEvent.from_date="{event_from_date}" ' \
            f'AND ComplexEvent.to_date="{event_to_date}";'

    @classmethod
    def insert_query(cls, *args):
        cpf = args[0]
        role = args[1]
        age = args[2]
        name = args[3]
        event_type = args[4]
        event_title = args[5]
        event_text = args[6]
        event_from_date = args[7]
        event_to_date = args[8]
        complex_name = args[9]

        employee_id = cls.select_parent(1, cpf, role, complex_name)
        if not employee_id:
            employee_id = cls.insert_parent(1, cpf, role, age, name, complex_name)

        event_id = cls.select_parent(0, event_type, event_title, complex_name)
        if not event_id:
            event_id = cls.insert_parent(0, event_type, event_title, event_text, complex_name)

        return f'INSERT INTO ComplexEvent (from_date, to_date, event_id, employee_id) ' \
            f'VALUES ("{event_from_date}", "{event_to_date}", {event_id}, {employee_id});'

    @classmethod
    def delete_query(cls, *args):
        event_type = args[0]
        event_title = args[1]
        event_from_date = args[3]
        event_to_date = args[4]
        complex_name = args[3]

        event_id = cls.select_parent(0, event_type, event_title, complex_name)
            
        return f'DELETE FROM ComplexEvent ' \
            f'WHERE ComplexEvent.from_date="{event_from_date}" AND ComplexEvent.to_date="{event_to_date}" AND ComplexEvent.event_id={event_id};'

    @classmethod
    def select_parent_query(cls, *args):
        parent_number = args[0]
        if parent_number == 0:
            event_type = args[1]
            event_title = args[2]
            complex_name = args[3]

            complex_id = cls.select_parent(2, complex_name)

            return f'SELECT id FROM Event WHERE Event.type="{event_type}" AND Event.title="{event_title}" AND Event.complex_id={complex_id};'

        elif parent_number == 1:
            cpf = args[1]
            role = args[2]
            complex_name = args[3]

            complex_id = cls.select_parent(2, complex_name)

            return f'SELECT id FROM Employee WHERE Employee.cpf="{cpf}" AND Employee.role="{role}" AND Employee.complex_id={complex_id};'

        elif parent_number == 2:
            complex_name = args[1]

            return f'SELECT id FROM Complex WHERE Complex.name="{complex_name}";'

        else:
            raise RuntimeError(f'Internal error on complex event parent selection. Arguments: {args}.')

    @classmethod
    def insert_parent_query(cls, *args):
        parent_number = args[0]
        if parent_number == 0:
            event_type = args[1]
            event_title = args[2]
            event_text = args[3]
            complex_name = args[4]

            complex_id = cls.select_parent(2, complex_name)
            if not complex_id:
                complex_id = cls.insert_parent(2, complex_name)

            return f'INSERT INTO Event (type, title, text, complex_id) VALUES ("{event_type}", "{event_title}", "{event_text}", {complex_id});'

        elif parent_number == 1:
            cpf = args[1]
            role = args[2]
            age = args[3]
            name = args[4]
            complex_name = args[5]

            complex_id = cls.select_parent(2, complex_name)
            if not complex_id:
                complex_id = cls.insert_parent(2, complex_name)

            return f'INSERT INTO Employee (cpf, role, age, name, complex_id) VALUES ("{cpf}", "{role}", {age}, "{name}", {complex_id})'

        elif parent_number == 2:
            complex_name = args[1]

            return f'INSERT INTO Complex (name) VALUES ("{complex_name}");'

        else:
            raise RuntimeError(f'Internal error on complex event parent insertion. Arguments: {args}.')
