from model.database import Base


class Apartment(Base):
    @classmethod
    def select_all_from_parent_query(cls, *args):
        tower_name = args[0]
        complex_name = args[1]

        tower_id = cls.select_parent(0, tower_name, complex_name)

        return f'SELECT * FROM Apartment WHERE Apartment.tower_id={tower_id};'

    @classmethod
    def select_one_query(cls, *args):
        apt_number = args[0]
        tower_name = args[1]
        complex_name = args[2]

        tower_id = cls.select_parent(0, tower_name, complex_name)

        return f'SELECT * FROM Apartment WHERE Apartment.number={apt_number} AND Apartment.tower_id={tower_id};'

    @classmethod
    def insert_query(cls, *args):
        apt_number = args[0]
        tower_name = args[1]
        complex_name = args[2]

        tower_id = cls.select_parent(0, tower_name, complex_name)
        if not tower_id:
            tower_id = cls.insert_parent(0, tower_name, complex_name)

        return f'INSERT INTO Apartment (number, tower_id) VALUES ({apt_number}, {tower_id});'

    @classmethod
    def delete_query(cls, *args):
        apt_number = args[0]
        tower_name = args[1]
        complex_name = args[2]

        tower_id = cls.select_parent(0, tower_name, complex_name)

        return f'DELETE FROM Apartment WHERE Apartment.number={apt_number} AND Apartment.tower_id={tower_id};'

    @classmethod
    def select_parent_query(cls, *args):
        parent_number = args[0]
        if parent_number == 0:
            tower_name = args[1]
            complex_name = args[2]

            complex_id = cls.select_parent(1, complex_name)

            return f'SELECT id FROM Tower WHERE Tower.name="{tower_name}" AND Tower.complex_id={complex_id};'

        elif parent_number == 1:
            complex_name = args[1]

            return f'SELECT id FROM Complex WHERE Complex.name="{complex_name}";'

        else:
            raise RuntimeError(f'Internal error on apartment parent selection. Arguments: {args}.')

    @classmethod
    def insert_parent_query(cls, *args):
        parent_number = args[0]
        if parent_number == 0:
            tower_name = args[1]
            complex_name = args[2]

            complex_id = cls.select_parent(1, complex_name)
            if not complex_id:
                complex_id = cls.insert_parent(1, complex_name)

            return f'INSERT INTO Tower (name, complex_id) VALUES ("{tower_name}", {complex_id});'

        elif parent_number == 1:
            complex_name = args[1]

            return f'INSERT INTO Complex (name) VALUES ("{complex_name}");'

        else:
            raise RuntimeError(f'Internal error on apartment parent insertion. Arguments: {args}.')
