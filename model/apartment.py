from model.database import Base


class Apartment(Base):
    @classmethod
    def __select_all_query(cls):
        return 'SELECT * FROM Apartment;'

    @classmethod
    def __select_one_query(cls, *args):
        apt_number = args[0]
        tower_number = args[0]
        return f'SELECT * FROM Apartment WHERE Apartment.apt_number={apt_number} AND Apartment.tower_number={tower_number};'

    @classmethod
    def __insert_query(cls, *args):
        apt_number = args[0]
        tower_number = args[0]

        if not cls.select_parent(tower_number):
            cls.insert_parent(tower_number)

        return f'INSERT INTO Apartment (apt_number, tower_number) VALUES ({apt_number}, {tower_number});'

    @classmethod
    def __delete_query(cls, *args):
        apartment_id = cls.select_one(args)[0]
        return f'DELETE FROM Apartment WHERE Apartment.apt_number={apartment_id};'

    @classmethod
    def __select_parent_query(cls, *args):
        return 'SELECT * FROM Apartment INNER JOIN TOWER ON TOWER.number = Apartment.tower_number;'

    @classmethod
    def __insert_parent_query(cls, *args):
        tower_number = args[0]
        return f'INSERT INTO TOWER (number) VALUES ({tower_number});'
