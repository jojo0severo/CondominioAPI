from model.database import Base


class ServiceDay(Base):
    @classmethod
    def select_all_from_parent_query(cls, *args):
        apt_number = args[0]
        tower_name = args[1]
        complex_name = args[2]

        apt_id = cls.select_parent(1, apt_number, tower_name, complex_name)

        return f'SELECT * FROM ServiceDay INNER JOIN Service ON ServiceDay.service_id = Service.id WHERE Service.apt_id={apt_id};'

    @classmethod
    def select_all_query(cls):
        return 'SELECT * FROM ServiceDay;'

    @classmethod
    def select_one_query(cls, *args):
        weekday = args[0]
        name = args[1]
        company = args[2]
        service_type = args[3]
        apt_number = args[4]
        tower_name = args[5]
        complex_name = args[6]

        service_id = cls.select_parent(0, name, company, service_type, apt_number, tower_name, complex_name)

        return f'SELECT * FROM ServiceDay WHERE ServiceDay.weekday={weekday} AND ServiceDay.service_id={service_id};'

    @classmethod
    def insert_query(cls, *args):
        weekday = args[0]
        from_date = args[1]
        to_date = args[2]
        name = args[3]
        company = args[4]
        service_type = args[5]
        apt_number = args[6]
        tower_name = args[7]
        complex_name = args[8]

        service_id = cls.select_parent(0, name, company, service_type, apt_number, tower_name, complex_name)
        if not service_id:
            service_id = cls.insert_parent(0, name, company, service_type, apt_number, tower_name, complex_name)

        return f'INSERT INTO ServiceDay (service_id, weekday, from_date, to_date) ' \
               f'VALUES ({service_id}, {weekday}, "{from_date}", "{to_date}");'

    @classmethod
    def delete_query(cls, *args):
        weekday = args[0]
        from_date = args[1]
        to_date = args[2]
        name = args[3]
        company = args[4]
        service_type = args[5]
        apt_number = args[6]
        tower_name = args[7]
        complex_name = args[8]

        service_id = cls.select_parent(0, name, company, service_type, apt_number, tower_name, complex_name)

        return f'DELETE FROM ServiceDay WHERE ServiceDay.weekday={weekday} ' \
               f'AND ServiceDay.from_date="{from_date}" AND ServiceDay.to_date="{to_date}" AND ServiceDay.service_id={service_id};'

    @classmethod
    def select_parent_query(cls, *args):
        parent_number = args[0]
        if parent_number == 0:
            name = args[1]
            company = args[2]
            service_type = args[3]
            apt_number = args[4]
            tower_name = args[5]
            complex_name = args[6]

            apt_id = cls.select_parent(1, apt_number, tower_name, complex_name)

            return f'SELECT * FROM Service ' \
                   f'WHERE Service.name="{name}" AND Service.company="{company}" AND Service.type="{service_type}" AND Service.apt_id={apt_id}'

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
            raise RuntimeError(f'Internal error on service day parent selection. Arguments: {args}.')

    @classmethod
    def insert_parent_query(cls, *args):
        parent_number = args[0]
        if parent_number == 0:
            name = args[1]
            company = args[2]
            service_type = args[3]
            apt_number = args[4]
            tower_name = args[5]
            complex_name = args[6]

            apt_id = cls.select_parent(1, apt_number, tower_name, complex_name)
            if not apt_id:
                apt_id = cls.insert_parent(1, apt_number, tower_name, complex_name)

            return f'INSERT INTO Service (name, company, type, apt_id) ' \
                   f'VALUES ("{name}", "{company}", "{service_type}", {apt_id});'

        elif parent_number == 1:
            apt_number = args[1]
            tower_name = args[2]
            complex_name = args[3]

            tower_id = cls.select_parent(2, tower_name, complex_name)
            if not tower_id:
                tower_id = cls.insert_parent(2, tower_name, complex_name)

            return f'INSERT INTO Apartment (number, tower_id) VALUES({apt_number}, {tower_id});'

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
            raise RuntimeError(f'Internal error on service day parent insertion. Arguments: {args}.')
