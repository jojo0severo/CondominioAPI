import base64
from helpers.permission_manager import PermissionManager
from helpers.formatter import JSONFormatter
from helpers.error_decorators import *


class Handler:
    def __init__(self, system_key):
        self.formatter = JSONFormatter()
        self.permission_manager = PermissionManager(system_key)

    @permission_error_decorator
    @key_error_decorator
    def login_resident(self, data, system_key):
        username = data['username']
        password = data['password']

        response = self.formatter.format_resident_connection(*self.permission_manager.login_resident(username, password, system_key))
        if response['result']:
            status = 200
            room = response['data']['condominium']['Name']
        else:
            status = 400
            room = None

        response['status'] = status

        return status, response, room

    @permission_error_decorator
    @key_error_decorator
    def login_employee(self, data, system_key):
        username = data['username']
        password = data['password']

        result, info = self.permission_manager.login_employee(username, password, system_key)
        response = self.formatter.format_employee_connection(result, info)
        if response['result']:
            status = 200
            room = response['data']['condominium']['Name']
        else:
            status = 409
            room = None

        response['status'] = status

        return status, response, room

    @permission_error_decorator
    @key_error_decorator
    def register_resident(self, data, system_key):
        username = data['username']
        password = data['password']
        cpf = data['cpf']
        name = data['name']
        birthday = data['birthday']
        apartment_id = data['apartment_id']

        if 'photo_location' not in data:
            photo_location = None
        else:
            photo_location = data['photo_location']

        result, info = self.permission_manager.register_resident(username, password, cpf, name, birthday, photo_location, apartment_id, system_key)
        response = self.formatter.format_resident_connection(result, info)

        if response['result']:
            status = 201
            room = response['data']['condominium']['Name']
        else:
            status = 409
            room = None

        response['status'] = status

        return status, response, room

    @permission_error_decorator
    @key_error_decorator
    def register_employee(self, data, system_key):
        username = data['username']
        password = data['password']
        cpf = data['cpf']
        name = data['name']
        birthday = data['birthday']
        role = data['role']
        condominium_id = data['condominium_id']

        if 'photo_location' not in data:
            photo_location = None
        else:
            photo_location = data['photo_location']

        result, info = self.permission_manager.register_employee(username, password, cpf, name, birthday, photo_location, role, condominium_id, system_key)
        response = self.formatter.format_employee_connection(result, info)
        if response['result']:
            status = 201
            room = response['data']['condominium']['Name']
        else:
            status = 400
            room = None

        response['status'] = status

        return status, response, room

    def get_employees(self, data, system_key, user_key):
        user_id = base64.urlsafe_b64decode(data['id'])
        return 500, {}

    def drop_session(self, system_key, session_key):
        return self.permission_manager.drop_session(system_key, session_key)
