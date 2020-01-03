from model.database import Base


class Item(Base):
    @classmethod
    def select_all_from_parent_query(cls, *args):
        shop_type = args[0]
        complex_name = args[1]

        shop_id = cls.select_parent(3, shop_type, complex_name)

        return f'SELECT * FROM Item WHERE Item.shop_id={shop_id};'

    @classmethod
    def select_all_query(cls):
        return 'SELECT * FROM Item;'

    @classmethod
    def select_one_query(cls, *args):
        shop_type = args[0]
        owner = args[1]
        name = args[2]
        complex_name = args[3]

        shop_id = cls.select_parent(3, shop_type, complex_name)

        return f'SELECT * FROM Item WHERE Item.shop_id={shop_id} AND Item.owner={owner} AND Item.name="{name}";'

    @classmethod
    def insert_query(cls, *args):
        shop_type = args[0]
        owner = args[1]
        name = args[2]
        price = args[3]
        description = args[4]
        images_folder = args[5]
        tower_name = args[6]
        complex_name = args[7]

        apt_id = cls.select_parent(0, owner, tower_name, complex_name)
        if not apt_id:
            apt_id = cls.insert_parent(0, owner, tower_name, complex_name)

        shop_id = cls.select_parent(3, shop_type, complex_name)
        if not shop_id:
            shop_id = cls.insert_parent(3, shop_type, complex_name)

        return f'INSERT INTO Item (shop_id, owner, name, price, description, images_folder) ' \
            f'VALUES ({shop_id}, {apt_id}, "{name}", {price}, "{description}", "{images_folder}");'

    @classmethod
    def delete_query(cls, *args):
        shop_type = args[0]
        owner = args[1]
        name = args[2]
        complex_name = args[3]

        shop_id = cls.select_parent(3, shop_type, complex_name)

        return f'DELETE FROM Item WHERE Item.shop_id={shop_id} AND Item.owner={owner} AND Item.name="{name}";'

    @classmethod
    def select_parent_query(cls, *args):
        parent_number = args[0]
        if parent_number == 0:
            owner = args[1]
            tower_name = args[2]
            complex_name = args[3]

            tower_id = cls.select_parent(1, tower_name, complex_name)

            return f'SELECT id FROM Apartment WHERE Apartment.id={owner} AND Apartment.tower_id={tower_id};'

        elif parent_number == 1:
            tower_name = args[1]
            complex_name = args[2]

            complex_id = cls.select_parent(2, complex_name)
            if not complex_id:
                complex_id = cls.insert_parent(2, complex_name)

            return f'SELECT id FROM Tower WHERE Tower.name="{tower_name}" AND Tower.complex_id={complex_id};'

        elif parent_number == 2:
            complex_name = args[1]

            return f'SELECT id FROM Complex WHERE Complex.name="{complex_name}";'

        elif parent_number == 3:
            shop_type = args[1]
            complex_name = args[2]

            complex_id = cls.select_parent(2, complex_name)
            if not complex_id:
                complex_id = cls.insert_parent(2, complex_name)

            return f'SELECT id FROM Shop WHERE Shop.type="{shop_type}" AND Shop.complex_id={complex_id};'

        else:
            raise RuntimeError(f'Internal error on shop item parent selection. Arguments: {args}.')

    @classmethod
    def insert_parent_query(cls, *args):
        parent_number = args[0]
        if parent_number == 0:
            owner = args[0]
            tower_id = args[1]
            complex_name = args[2]

            if not cls.select_parent(1, tower_id, complex_name):
                cls.insert_parent(1, tower_id, complex_name)

            return f'INSERT INTO Apartment (number, tower_id) VALUES ({owner}, "{tower_id}");'

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

        elif parent_number == 3:
            shop_type = args[1]
            complex_name = args[2]

            complex_id = cls.select_parent(2, complex_name)
            if not complex_id:
                complex_id = cls.insert_parent(2, complex_name)

            return f'INSERT INTO Shop (type, complex_id) VALUES ("{shop_type}", {complex_id});'

        else:
            raise RuntimeError(f'Internal error on shop item parent selection. Arguments: {args}.')