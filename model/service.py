from model.database import Base


class Service(Base):
    @classmethod
    def select_all_from_parent_query(cls, *args):
        parent_number = args[0]
        apt_number = args[1]
        tower_name = args[2]
        complex_name = args[3]

        if parent_number == 0:
            apt_id = cls.select_parent(0, apt_number, tower_name, complex_name)
            return f'SELECT * FROM Service WHERE Service.apt_id={apt_id};'

        elif parent_number == 1:
            tower_id = cls.select_parent(1, tower_name, complex_name)
            return f'SELECT Service.id, Service.name, Service.company, Service.type FROM Service ' \
                   f'INNER JOIN Apartment on Service.apt_id=Apartment.id ' \
                   f'WHERE Apartment.tower_id={tower_id}'

        elif parent_number == 2:
            complex_id = cls.select_parent(2, complex_name)
            return f'SELECT Service.id, Service.name, Service.company, Service.type FROM Service ' \
                   f'INNER JOIN Apartment ON Service.apt_id=Apartment.id ' \
                   f'INNER JOIN Tower ON Apartment.tower_id=Tower.id ' \
                   f'WHERE Tower.complex_id={complex_id}'

        else:
            raise ValueError('Wrong parent number given')

    @classmethod
    def select_one_query(cls, *args):
        name = args[0]
        company = args[1]
        service_type = args[2]

        return f'SELECT * FROM Service WHERE Service.name="{name}" AND Service.company="{company}" AND Service.type="{service_type}";'

    @classmethod
    def insert_query(cls, *args):
        name = args[0]
        company = args[1]
        service_type = args[2]
        apt_number = args[3]
        tower_name = args[4]
        complex_name = args[5]

        apt_id = cls.select_parent(0, apt_number, tower_name, complex_name)
        if not apt_id:
            apt_id = cls.insert_parent(0, apt_number, tower_name, complex_name)

        return f'INSERT INTO Service (name, company, type, apt_id) ' \
               f'VALUES ("{name}", "{company}", "{service_type}", {apt_id});'

    @classmethod
    def delete_query(cls, *args):
        name = args[0]
        company = args[1]
        service_type = args[2]

        return f'DELETE FROM Service WHERE Service.name="{name}" AND Service.company="{company}" AND Service.type="{service_type}";'

    @classmethod
    def select_parent_query(cls, *args):
        parent_number = args[0]
        if parent_number == 0:
            apt_number = args[1]
            tower_name = args[2]
            complex_name = args[3]

            tower_id = cls.select_parent(1, tower_name, complex_name)

            return f'SELECT id FROM Apartment WHERE Apartment.number={apt_number} AND Apartment.tower_id={tower_id};'

        elif parent_number == 1:
            tower_name = args[1]
            complex_name = args[2]

            complex_id = cls.select_parent(2, complex_name)

            return f'SELECT id FROM Tower WHERE Tower.name="{tower_name}" AND Tower.complex_id={complex_id};'

        elif parent_number == 2:
            complex_name = args[1]

            return f'SELECT id FROM Complex WHERE Complex.name="{complex_name}";'

        else:
            raise RuntimeError(f'Internal error on service parent selection. Arguments: {args}.')

    @classmethod
    def insert_parent_query(cls, *args):
        parent_number = args[0]
        if parent_number == 0:
            apt_number = args[1]
            tower_name = args[2]
            complex_name = args[3]

            tower_id = cls.select_parent(1, tower_name, complex_name)
            if not tower_id:
                tower_id = cls.insert_parent(1, tower_name, complex_name)

            return f'INSERT INTO Apartment (number, tower_id) VALUES({apt_number}, {tower_id});'

        elif parent_number == 1:
            tower_name = args[1]
            complex_name = args[2]

            complex_id = cls.select_parent(2, complex_name)
            if not complex_id:
                complex_id = cls.insert_parent(2, complex_name)

            return f'INSERT INTO Tower (name, complex_id) VALUES ("{tower_name}", {complex_id});'

        elif parent_number == 2:
            complex_name = args[1]

            return f'INSERT INTO Complex (name) VALUES ("{complex_name}");'

        else:
            raise RuntimeError(f'Internal error on service parent insertion. Arguments: {args}.')
