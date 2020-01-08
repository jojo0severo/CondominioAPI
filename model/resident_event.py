from model.database import Base


class ResidentEvent(Base):
    @classmethod
    def select_all_from_parent_query(cls, *args):
        complex_name = args[0]
        if len(args) > 1:
            from_date = args[1]
            to_date = args[2]
            return f'SELECT Event.type, Event.title, Event.text, ResidentEvent.from_date, ResidentEvent.to_date ' \
                   f'FROM ResidentEvent ' \
                   f'INNER JOIN Event ON ResidentEvent.event_id = Event.id ' \
                   f'INNER JOIN Complex ON Event.complex_id = Complex.id ' \
                   f'WHERE Complex.name="{complex_name}" AND ' \
                   f'ResidentEvent.from_date>="{from_date}" AND ResidentEvent.to_date<="{to_date}";'

        return f'SELECT Event.type, Event.title, Event.text, ResidentEvent.from_date, ResidentEvent.to_date ' \
               f'FROM ResidentEvent ' \
               f'INNER JOIN Event ON ResidentEvent.event_id = Event.id ' \
               f'INNER JOIN Complex ON Event.complex_id = Complex.id ' \
               f'WHERE Complex.name="{complex_name}";'

    @classmethod
    def select_one_query(cls, *args):
        event_type = args[0]
        event_title = args[1]
        event_from_date = args[2]
        event_to_date = args[3]
        complex_name = args[4]

        event_id = cls.select_parent(0, event_type, event_title, complex_name)

        return f'SELECT * FROM ResidentEvent ' \
               f'WHERE ResidentEvent.event_id={event_id} AND ResidentEvent.from_date="{event_from_date}" ' \
               f'AND ResidentEvent.to_date="{event_to_date}";'

    @classmethod
    def insert_query(cls, *args):
        apt_number = args[0]
        tower_name = args[1]
        event_type = args[2]
        event_title = args[3]
        event_text = args[4]
        event_from_date = args[5]
        event_to_date = args[6]
        complex_name = args[7]

        apt_id = cls.select_parent(1, apt_number, tower_name, complex_name)
        if not apt_id:
            apt_id = cls.insert_parent(1, apt_number, tower_name, complex_name)

        event_id = cls.select_parent(0, event_type, event_title, complex_name)
        if not event_id:
            event_id = cls.insert_parent(0, event_type, event_title, event_text, complex_name)

        return f'INSERT INTO ResidentEvent (from_date, to_date, event_id, apt_id) ' \
               f'VALUES ("{event_from_date}", "{event_to_date}", {event_id}, {apt_id});'

    @classmethod
    def delete_query(cls, *args):
        event_type = args[0]
        event_title = args[1]
        event_from_date = args[3]
        event_to_date = args[4]
        complex_name = args[3]

        event_id = cls.select_parent(0, event_type, event_title, complex_name)

        return f'DELETE FROM ResidentEvent ' \
               f'WHERE ResidentEvent.from_date="{event_from_date}" AND ResidentEvent.to_date="{event_to_date}" ' \
               f'AND ResidentEvent.event_id={event_id};'

    @classmethod
    def select_parent_query(cls, *args):
        parent_number = args[0]
        if parent_number == 0:
            event_type = args[1]
            event_title = args[2]
            complex_name = args[3]

            complex_id = cls.select_parent(3, complex_name)

            return f'SELECT id FROM Event WHERE Event.type="{event_type}" AND Event.title="{event_title}" AND Event.complex_id={complex_id};'

        elif parent_number == 1:
            apt_number = args[1]
            tower_name = args[2]
            complex_name = args[3]

            tower_id = cls.select_parent(2, tower_name, complex_name)

            return f'SELECT id FROM Apartment WHERE Apartment.number={apt_number} AND Apartment.tower_id={tower_id};'

        elif parent_number == 2:
            tower_name = args[1]
            complex_name = args[2]

            complex_id = cls.select_parent(3, complex_name)

            return f'SELECT id FROM Tower WHERE Tower.name="{tower_name}" AND Tower.complex_id={complex_id};'

        elif parent_number == 3:
            complex_name = args[1]

            return f'SELECT id FROM Complex WHERE Complex.name="{complex_name}";'

        else:
            raise RuntimeError(f'Internal error on resident event parent selection. Arguments: {args}.')

    @classmethod
    def insert_parent_query(cls, *args):
        parent_number = args[0]
        if parent_number == 0:
            event_type = args[1]
            event_title = args[2]
            event_text = args[3]
            complex_name = args[4]

            complex_id = cls.select_parent(3, complex_name)
            if not complex_id:
                complex_id = cls.insert_parent(3, complex_name)

            return f'INSERT INTO Event (type, title, text, complex_id) VALUES ("{event_type}", "{event_title}", "{event_text}", {complex_id});'

        elif parent_number == 1:
            apt_number = args[1]
            tower_name = args[2]
            complex_name = args[3]

            tower_id = cls.select_parent(2, tower_name, complex_name)
            if not tower_id:
                tower_id = cls.insert_parent(2, tower_name, complex_name)

            return f'INSERT INTO Apartment (number, tower_id) VALUES ({apt_number}, {tower_id});'

        elif parent_number == 2:
            tower_name = args[1]
            complex_name = args[2]

            complex_id = cls.select_parent(3, complex_name)
            if not complex_id:
                complex_id = cls.insert_parent(3, complex_name)

            return f'INSERT INTO Tower (name, complex_id) VALUES ("{tower_name}", {complex_id});'

        elif parent_number == 3:
            complex_name = args[1]

            return f'INSERT INTO Complex (name) VALUES ("{complex_name}");'

        else:
            raise RuntimeError(f'Internal error on resident event parent insertion. Arguments: {args}.')
