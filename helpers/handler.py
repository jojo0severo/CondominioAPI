import base64
import bcrypt
from helpers.permission_manager import PermissionManager
from helpers.formatter import JSONFormatter
from helpers.general_error_decorators import *


class Handler:
    def __init__(self):
        self.formatter = JSONFormatter()
        self.permission_manager = PermissionManager()

    @runtime_error_decorator
    def register_key(self, key_type, key):
        self.permission_manager.register_key(key_type, key)

    @runtime_error_decorator
    @key_error_decorator
    def login_resident(self, data):
        username = data['username']
        password = data['password']

        result, info = self.permission_manager.login_resident(username, password)
        response, room = self.formatter.format_resident_connection(result, info, {'success': 200, 'failure': 400, 'empty': 404})

        return response['status'], response, room

    @runtime_error_decorator
    @key_error_decorator
    def login_employee(self, data):
        username = data['username']
        password = data['password']

        result, info = self.permission_manager.login_employee(username, password)
        response, room = self.formatter.format_employee_connection(result, info, {'success': 200, 'failure': 400, 'empty': 404})

        return response['status'], response, room

    @runtime_error_decorator
    @key_error_decorator
    def register_resident(self, data):
        username = data['username']
        password = bcrypt.hashpw(data['password'], bcrypt.gensalt())
        cpf = data['cpf']
        name = data['name']
        birthday = data['birthday']
        apartment_id = data['apartment_id']

        if 'photo_location' not in data:
            photo_location = None
        else:
            photo_location = data['photo_location']

        result, info = self.permission_manager.register_resident(username, password, cpf, name, birthday, photo_location, apartment_id)
        response, room = self.formatter.format_resident_connection(result, info, {'success': 201, 'failure': 409, 'empty': 404})

        return response['status'], response, room

    @runtime_error_decorator
    @key_error_decorator
    def register_employee(self, data):
        username = data['username']
        password = bcrypt.hashpw(data['password'], bcrypt.gensalt())
        cpf = data['cpf']
        name = data['name']
        birthday = data['birthday']
        role = data['role']
        condominium_id = data['condominium_id']

        if 'photo_location' not in data:
            photo_location = None
        else:
            photo_location = data['photo_location']

        result, info = self.permission_manager.register_employee(username, password, cpf, name, birthday, photo_location, role, condominium_id)
        response, room = self.formatter.format_employee_connection(result, info, {'success': 201, 'failure': 409, 'empty': 404})

        return response['status'], response, room

    @runtime_error_decorator
    @key_error_decorator
    def get_employees(self, data, user_key):
        user_id = int(base64.urlsafe_b64decode(data['user_id']).decode('ascii'))

        result, info = self.permission_manager.get_employees(user_id, user_key)
        response = self.formatter.format_employees(result, info, {'success': 200, 'failure': 403, 'empty': 404})

        return response['status'], response

    @runtime_error_decorator
    @key_error_decorator
    def get_residents(self, data, user_key):
        user_id = int(base64.urlsafe_b64decode(data['user_id']).decode('ascii'))
        apartment_number = data['apartment_number']

        result, info = self.permission_manager.get_residents(user_id, apartment_number, user_key)
        response = self.formatter.format_residents(result, info, {'success': 200, 'failure': 403, 'empty': 404})

        return response['status'], response

    @runtime_error_decorator
    @key_error_decorator
    def get_events(self, data, user_type, search_type, user_key):
        if user_type not in ['employee', 'resident']:
            raise ValueError(f'user_type: "{user_type}"')

        if search_type == 'all':
            user_id = int(base64.urlsafe_b64decode(data['user_id']).decode('ascii'))
            result, info = self.permission_manager.get_condominium_events(user_id)

        elif search_type in ['mine', 'apartment']:
            user_id = int(base64.urlsafe_b64decode(data['user_id']).decode('ascii'))
            if 'apartment_number' in data:
                apartment_number = data['apartment_number']
            else:
                apartment_number = None

            result, info = self.permission_manager.get_apartment_events(user_id, apartment_number, user_key)

        else:
            raise ValueError(f'search_type: "{search_type}"')

        response = self.formatter.format_events(result, info, {'success': 200, 'failure': 403, 'empty': 404})
        return response['status'], response

    @runtime_error_decorator
    def drop_session(self, session_key):
        return self.permission_manager.drop_session(session_key)















