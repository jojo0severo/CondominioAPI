from model.resident import Resident
from model.username import Username
from model.resident_user import ResidentUser
from setup import db
from sqlalchemy import exc, and_
import datetime


class ResidentController:
    def do_login(self, username):
        return ResidentUser.query.filter_by(username=username).first()

    def get_resident_by_id(self, resident_id):
        return Resident.query.get(resident_id)

    def get_resident_user_by_resident(self, cpf, apartment_id):
        return Resident.query.filter(and_(Resident.cpf == cpf, Resident.apartment_id == apartment_id)).first()

    def register_resident(self, username, hash_password, cpf, name, birthday, photo_location, apartment_id):
        try:
            birthday = datetime.datetime.strptime(birthday, '%Y-%m-%d')
            resident = Resident(cpf=cpf, name=name, birthday=birthday, photo_location=photo_location, apartment_id=apartment_id)
            resident_user = ResidentUser(password=hash_password)
            resident_user._username = Username(username=username)
            resident.user = resident_user

            db.session.add(resident)
            db.session.commit()

            return resident

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_resident(self, resident):
        try:
            db.session.delete(resident)
            db.session.commit()

            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False
