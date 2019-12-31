from model.database import Base


class Apartment(Base):
    @classmethod
    def select_all_query(cls):
        return 'SELECT * FROM Apartment;'

    @classmethod
    def select_one_query(cls, *args):
        apt_id= args[0]
        tower_id = args[0]
        return f'SELECT * FROM Apartment WHERE Apartment.id={apt_id} AND Apartment.tower_id="{tower_id}";'

    @classmethod
    def insert_query(cls, *args):
        apt_id = args[0]
        tower_id = args[1]
        complex_name = args[2]

        if not cls.select_parent(0, tower_id, complex_name):
            cls.insert_parent(0, tower_id, complex_name)

        return f'INSERT INTO Apartment (id, tower_id) VALUES ({apt_id}, "{tower_id}");'

    @classmethod
    def delete_query(cls, *args):
        apt_id = args[0]
        tower_id = args[1]

        return f'DELETE FROM Apartment WHERE Apartment.id={apt_id } AND Apartment.tower_id="{tower_id}";'

    @classmethod
    def select_parent_query(cls, *args):
        parent_number = args[0]
        if parent_number == 0:
            tower_id = args[1]
            complex_name = args[2]

            complex_id = cls.select_parent(1, complex_name)
            if not complex_id:
                complex_id = cls.insert_parent(1, complex_name)

            return f'SELECT id FROM Tower WHERE Tower.id="{tower_id}" AND Tower.complex_id={complex_id};'

        elif parent_number == 1:
            complex_name = args[1]

            return f'SELECT id FROM Complex WHERE Complex.name="{complex_name}";'

        else:
            raise RuntimeError(f'Internal error on apartment parent selection. Arguments: {args}.')

    @classmethod
    def insert_parent_query(cls, *args):
        parent_number = args[0]
        if parent_number == 0:
            tower_id = args[1]
            complex_name = args[2]

            complex_id = cls.select_parent(1, complex_name)
            if not complex_id:
                complex_id = cls.insert_parent(1, complex_name)

            return f'INSERT INTO Tower (id, complex_id) VALUES ("{tower_id}", {complex_id});'

        elif parent_number == 1:
            complex_name = args[1]

            return f'INSERT INTO Complex (name) VALUES ("{complex_name}");'

        else:
            raise RuntimeError(f'Internal error on apartment parent insertion. Arguments: {args}.')
