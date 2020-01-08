import sqlite3

db_location = 'data/database.db'


def setup_database():
    import os
    os.makedirs('data/', exist_ok=True)

    try:
        db = sqlite3.connect(db_location)
        db.executescript(open('resources/schema.sql', 'r').read())
        db.commit()

    except sqlite3.OperationalError as e:
        print(e)
        pass


class Base:
    @classmethod
    def select_parent(cls, *args):
        with sqlite3.connect(db_location) as conn:
            cursor = conn.cursor()
            query = cls.select_parent_query(*args)
            cursor.execute(query)
            result = cursor.fetchone()
            return result[0] if result else 0

    @classmethod
    def insert_parent(cls, *args):
        with sqlite3.connect(db_location) as conn:
            cursor = conn.cursor()
            query = cls.insert_parent_query(*args)
            cursor.execute(query)
            return cursor.lastrowid

    @classmethod
    def select_one(cls, *args):
        with sqlite3.connect(db_location) as conn:
            cursor = conn.cursor()
            query = cls.select_one_query(*args)
            cursor.execute(query)
            result = cursor.fetchone()
            return result[0] if result else ()

    @classmethod
    def select_all_from_parent(cls, *args):
        with sqlite3.connect(db_location) as conn:
            cursor = conn.cursor()
            query = cls.select_all_from_parent_query(*args)
            cursor.execute(query)
            return cursor.fetchall()

    @classmethod
    def insert(cls, *args):
        with sqlite3.connect(db_location) as conn:
            query = cls.insert_query(*args)
            conn.execute(query)

    @classmethod
    def delete(cls, *args):
        with sqlite3.connect(db_location) as conn:
            query = cls.delete_query(*args)
            conn.execute(query)

    @classmethod
    def select_parent_query(cls, *args):
        raise NotImplementedError

    @classmethod
    def insert_parent_query(cls, *args):
        raise NotImplementedError

    @classmethod
    def select_one_query(cls, *args):
        raise NotImplementedError

    @classmethod
    def select_all_from_parent_query(cls, *args):
        raise NotImplementedError

    @classmethod
    def insert_query(cls, *args):
        raise NotImplementedError

    @classmethod
    def delete_query(cls, *args):
        raise NotImplementedError
