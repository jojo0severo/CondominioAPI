from model.employee import Employee
from model.username import Username
from model.employee_user import EmployeeUser
from setup import db
from sqlalchemy import exc, and_
import bcrypt
import datetime


class EmployeeController:
    def do_login(self, username):
        return EmployeeUser.query.filter_by(username=username).first()

    def get_employee_by_id(self, employee_id):
        return Employee.query.get(employee_id)

    def get_employee_user_by_employee(self, cpf, role, condominium_id):
        return Employee.query.filter(and_(Employee.cpf == cpf, Employee.role == role, Employee.condominium_id == condominium_id)).first()

    def get_employees_by_condominium_id(self, condominium_id):
        return Employee.query.filter_by(condominium_id=condominium_id).all()

    def register_employee(self, username, hash_password, cpf, name, birthday, photo_location, role, condominium_id):
        try:
            birthday = datetime.datetime.strptime(birthday, '%Y-%m-%d')
            employee = Employee(cpf=cpf, name=name, birthday=birthday, photo_location=photo_location, role=role, condominium_id=condominium_id)
            employee_user = EmployeeUser(password=hash_password)
            employee_user._username = Username(username=username)
            employee.user = employee_user

            db.session.add(employee)
            db.session.commit()

            return employee

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_employee(self, employee):
        try:
            db.session.delete(employee)
            db.session.commit()

            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False
