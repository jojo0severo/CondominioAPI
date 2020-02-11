from model.employee import Employee
from model.employee_user import EmployeeUser
from setup import db
from sqlalchemy import exc, and_
import datetime


class EmployeeController:
    def do_login(self, username, password):
        user = EmployeeUser.query.get(username)
        return user is not None and user.password == password, user.employee

    def get_employee_by_id(self, employee_id):
        employee = Employee.query.get(employee_id)
        if not employee:
            raise ReferenceError

        return employee

    def get_employee_user_by_employee(self, cpf, name, role, birthday, condominium_id):
        employee = Employee.query.filter(and_(
            Employee.cpf == cpf, Employee.role == role, Employee.condominium_id == condominium_id)
        ).first()

        if not employee:
            raise ReferenceError

        if employee.name != name or employee.birthday != birthday:
            raise PermissionError

        return employee.user

    def register_employee(self, username, password, cpf, name, birthday, photo_location, role, condominium_id):
        try:
            birthday = datetime.datetime.strptime(birthday, '%Y-%m-%d')
            employee = Employee(cpf=cpf, name=name, birthday=birthday, photo_location=photo_location, role=role, condominium_id=condominium_id)
            employee.user = EmployeeUser(username=username, password=password)

            db.session.add(employee)
            db.session.commit()

        except exc.IntegrityError:
            db.session.rollback()
            return False, None

        return True, employee

    def remove_employee(self, username, password, cpf, name, role, birthday, condominium_id):
        employee_user = EmployeeUser.query.get(username)
        if not employee_user:
            raise ReferenceError

        if employee_user.passowrd != password:
            raise PermissionError

        employee = Employee.query.filter(and_(Employee.cpf == cpf, Employee.role == role, Employee.condominium_id == condominium_id)).first()
        if not employee:
            raise ReferenceError

        if employee.name != name or employee.birthday != birthday:
            raise PermissionError

        db.session.delete(employee_user)
        db.session.delete(employee)
        db.session.commit()
