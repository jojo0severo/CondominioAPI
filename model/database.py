import sqlite3

db_location = 'data/database.db'


def setup_database():
    import os
    os.makedirs('data/', exist_ok=True)

    try:
        db = sqlite3.connect(db_location)
        db.executescript(open('resources/schema.sql', 'r').read())
        db.commit()

    except sqlite3.OperationalError:
        pass


class Base:
    @classmethod
    def select_parent(cls, *args):
        with sqlite3.connect(db_location).cursor() as cursor:
            cursor.execute(cls.__select_parent_query(args))
            return cursor.fetchone()

    @classmethod
    def insert_parent(cls, *args):
        with sqlite3.connect(db_location).cursor() as cursor:
            cursor.execute(cls.__insert_parent_query(args))

    @classmethod
    def select_one(cls, *args):
        with sqlite3.connect(db_location).cursor() as cursor:
            cursor.execute(cls.__select_one_query(args))
            return cursor.fetchone()

    @classmethod
    def select_all(cls):
        with sqlite3.connect(db_location).cursor() as cursor:
            cursor.execute(cls.__select_all_query())
            return cursor.fetchall()

    @classmethod
    def insert(cls, *args):
        with sqlite3.connect(db_location) as conn:
            conn.execute(cls.__insert_query(args))

    @classmethod
    def delete(cls, *args):
        with sqlite3.connect(db_location) as conn:
            conn.execute(cls.__delete_query(args))

    @classmethod
    def __select_all_query(cls):
        return ''

    @classmethod
    def __select_one_query(cls, *args):
        return ''

    @classmethod
    def __insert_query(cls, *args):
        return ''

    @classmethod
    def __delete_query(cls, *args):
        return ''

    @classmethod
    def __select_parent_query(cls, *args):
        return ''

    @classmethod
    def __insert_parent_query(cls, *args):
        return ''
