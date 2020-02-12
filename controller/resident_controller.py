from model.resident import Resident
from model.resident_user import ResidentUser
from setup import db
from sqlalchemy import exc, and_
import bcrypt
import datetime


class ResidentController:
    def do_login(self, username, password):
        user = ResidentUser.query.get(username)
        if user is not None:
            if bcrypt.checkpw(password.encode('utf-8'), user.password):
                return True, user.resident

        return False, None

    def get_resident_by_id(self, resident_id):
        resident = Resident.query.get(resident_id)
        if not resident:
            raise ReferenceError

        return resident

    def get_resident_user_by_resident(self, cpf, name, birthday, apartment_id):
        resident = Resident.query.filter(and_(Resident.cpf == cpf, Resident.apartment_id == apartment_id)).first()
        if not resident:
            raise ReferenceError

        if resident.name != name or resident.birthday != birthday:
            raise PermissionError

        return resident.user

    def register_resident(self, username, password, cpf, name, birthday, photo_location, apartment_id):
        try:
            birthday = datetime.datetime.strptime(birthday, '%Y-%m-%d')
            resident = Resident(cpf=cpf, name=name, birthday=birthday, photo_location=photo_location, apartment_id=apartment_id)
            resident.user = ResidentUser(username=username, password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))

            db.session.add(resident)
            db.session.commit()

        except exc.IntegrityError:
            db.session.rollback()
            return False, None

        return True, resident

    def remove_resident(self, username, password, cpf, name, birthday, apartment_id):
        resident_user = ResidentUser.query.get(username)
        if not resident_user:
            raise ReferenceError

        if not bcrypt.checkpw(password.encode('utf-8'), resident_user.password):
            raise PermissionError

        resident = Resident.query.filter(and_(Resident.cpf == cpf, Resident.apartment_id == apartment_id)).first()
        if not resident:
            raise ReferenceError

        if resident.name != name or resident.birthday.strftime("%Y-%m-%d") != birthday:
            raise PermissionError

        db.session.delete(resident_user)
        db.session.delete(resident)
        db.session.commit()
