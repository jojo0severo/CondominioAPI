from helpers.permission_manager import PermissionManager
from helpers.formatter import JSONFormatter
import bcrypt
from functools import wraps
import base64


def key_error_decorator(func):
    @wraps(func)
    def handle_key_error(*args):
        try:
            return func(*args)
        except KeyError as e:
            return 400, {'status': 400, 'result': False, 'event': f'Missing information: {e}', 'data': {}}

    return handle_key_error


def runtime_error_decorator(func):
    @wraps(func)
    def handle_runtime_error(*args):
        try:
            return func(*args)
        except RuntimeError as e:
            return 500, {'status': 500, 'result': False, 'event': f'Something went wrong with the application: {e}', 'data': {}}

    return handle_runtime_error


def value_error_decorator(func):
    @wraps(func)
    def handle_value_error(*args):
        try:
            return func(*args)
        except ValueError as e:
            return 400, {'status': 400, 'result': False, 'event': f'Attribute type error: {e}', 'data': {}}

    return handle_value_error


def type_error_decorator(func):
    @wraps(func)
    def handle_type_error(*args):
        try:
            return func(*args)
        except ValueError as e:
            return 400, {'status': 400, 'result': False, 'event': f'Unknown option passed: {e}', 'data': {}}

    return handle_type_error


class Handler:
    def __init__(self):
        self.formatter = JSONFormatter()
        self.permission_manager = PermissionManager()

    @runtime_error_decorator
    def register_key(self, key_type, key):
        self.permission_manager.register_key(key_type, key)

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def login_super_user(self, data):
        username = data['username']
        password = data['password']

        result, info, id_ = self.permission_manager.login_super_user(username, password)
        status, response = self.formatter.format_super_user_connection(result, info, {'success': 200, 'failure': 401})

        return status, response, id_

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def build_condominium_schema(self, schema, user_key):
        result, info = self.permission_manager.build_condominium_schema(schema, user_key)
        if result:
            return 200, self.formatter.response(200, 'Success')

        return 400, self.formatter.response(400, 'Failure', 'Condominium could not be built')

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def login_resident(self, data):
        username = data['username']
        password = data['password']

        result, info, apt_id, room = self.permission_manager.login_resident(username, password)
        status, response = self.formatter.format_resident_login(result, info, {'success': 200, 'failure': 400, 'empty': 404})

        return status, response, room, apt_id

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def login_employee(self, data):
        username = data['username']
        password = data['password']

        result, info, login_type = self.permission_manager.login_employee(username, password)
        response, room, employee_id = self.formatter.format_employee_connection(result, info, {'success': 200, 'failure': 400, 'empty': 404})

        return response['status'], response, room, employee_id, login_type

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def register_resident(self, data, father_id, user_key):
        cpf = data['cpf']
        name = data['name']
        birthday = data['birthday']

        if 'photo_location' not in data:
            photo_location = None
        else:
            photo_location = data['photo_location']

        result, info = self.permission_manager.register_resident(cpf, name, birthday, photo_location, father_id, user_key)
        response = self.formatter.format_resident_connection(result, info, {'success': 201, 'failure': 409, 'empty': 404})

        return response['status'], response

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def register_resident_user(self, data, father_id, user_key):
        username = data['username']
        password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt(rounds=6)).decode('utf-8')
        apartment_id = int(base64.urlsafe_b64decode(data['apartment_id']).decode('ascii'))

        result, info = self.permission_manager.register_resident_user(username, password, apartment_id, father_id, user_key)
        if result:
            return 200, self.formatter.response(200, 'Success')

        return 400, self.formatter.response(400, 'Failure', info)

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def register_employee(self, data, father_id, user_key):
        employee_type = data['employee_type']
        username = data['username']
        password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt(rounds=6)).decode('utf-8')
        cpf = data['cpf']
        name = data['name']
        birthday = data['birthday']
        role = data['role']

        if 'photo_location' not in data:
            photo_location = None
        else:
            photo_location = data['photo_location']

        if 'condominium_id' in data:
            father_id = int(base64.urlsafe_b64decode(data['condominium_id']).decode('ascii'))

        result, info = self.permission_manager.register_employee(employee_type, username, password, cpf, name, birthday, photo_location, role, father_id, user_key)
        response, _, _ = self.formatter.format_employee_connection(result, info, {'success': 201, 'failure': 409, 'empty': 404})

        return response['status'], response

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def get_employees(self, user_id, user_key):
        result, info = self.permission_manager.get_employees(user_id, user_key)
        response = self.formatter.format_employees(result, info, {'success': 200, 'failure': 403, 'empty': 404})

        return response['status'], response

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def get_residents(self, data, father_id, user_key):
        try:
            user_id = int(base64.urlsafe_b64decode(data['user_id']).decode('ascii'))
        except ValueError:
            return 190, self.formatter.response(400, 'Failure', 'Incorrect ID format informed')

        apartment_number = data['apartment_number']

        result, info = self.permission_manager.get_residents(user_id, apartment_number, father_id, user_key)
        response = self.formatter.format_residents(result, info, {'success': 200, 'failure': 403, 'empty': 404})

        return response['status'], response

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def get_notifications(self, father_id, user_key):
        result, info = self.permission_manager.get_notifications(father_id, user_key)
        response = self.formatter.format_notifications(result, info, {'success': 200, 'failure': 403, 'empty': 404})

        return response['status'], response

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def get_guests(self, data, father_id, user_key):
        apartment_id = data.get('apartment_id')
        if apartment_id is not None:
            try:
                apartment_id = int(base64.urlsafe_b64decode(apartment_id).decode('ascii'))
            except ValueError:
                return 190, self.formatter.response(400, 'Failure', 'Incorrect ID format informed')

        result, info = self.permission_manager.get_guests(apartment_id, father_id, user_key)
        response = self.formatter.format_guests(result, info, {'success': 200, 'failure': 403, 'empty': 404})

        return response['status'], response

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def get_services(self, data, father_id, user_key):
        apartment_id = data.get('apartment_id')
        if apartment_id is not None:
            try:
                apartment_id = int(base64.urlsafe_b64decode(apartment_id).decode('ascii'))
            except ValueError:
                return 190, self.formatter.response(400, 'Failure', 'Incorrect ID format informed')

        result, info = self.permission_manager.get_services(apartment_id, father_id, user_key)
        response = self.formatter.format_services(result, info, {'success': 200, 'failure': 403, 'empty': 404})

        return response['status'], response

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def get_rules(self, father_id, user_key):
        result, info = self.permission_manager.get_rules(father_id, user_key)
        response = self.formatter.format_rules(result, info, {'success': 200, 'failure': 403, 'empty': 404})

        return response['status'], response

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def get_events(self, data, father_id, user_key):
        apartment_id = data.get('apartment_id')
        if apartment_id is not None:
            try:
                apartment_id = int(base64.urlsafe_b64decode(apartment_id).decode('ascii'))
                result, info = self.permission_manager.get_apartment_events(apartment_id, father_id, user_key)
            except ValueError:
                return 190, self.formatter.response(400, 'Failure', 'Incorrect ID format informed')

        else:
            start = data['start']
            end = data['end']
            result, info = self.permission_manager.get_all_events(start, end, father_id, user_key)

        response = self.formatter.format_events(result, info, {'success': 200, 'failure': 403, 'empty': 404})

        return response['status'], response

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def get_event_types(self, father_id, user_key):
        result, info = self.permission_manager.get_event_types(father_id, user_key)
        response = self.formatter.format_events(result, info, {'success': 200, 'failure': 403, 'empty': 404})

        return response['status'], response

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def register_notification(self, data, father_id, user_key):
        notification_type = int(data['notification_type'])
        title = data['title']
        text = data['text']
        finish_date = data['finish_date']

        result, info = self.permission_manager.register_notification(notification_type, title, text, finish_date, father_id, user_key)
        if result:
            return 201, self.formatter.response(201, 'Success')

        return 400, self.formatter.response(400, 'Failure', info)

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def register_guest(self, data, father_id, user_key):
        guest_name = data['name']
        guest_arrival = data['arrival']

        result, info = self.permission_manager.register_guest(guest_name, guest_arrival, father_id, user_key)
        if result:
            return 201, self.formatter.response(201, 'Success')

        return 400, self.formatter.response(400, 'Failure', info)

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def register_service(self, data, father_id, user_key):
        service_name = data['name']
        employee_name = data['employee']
        service_arrival = data['arrival']

        result, info = self.permission_manager.register_service(service_name, employee_name, service_arrival, father_id, user_key)
        if result:
            return 201, self.formatter.response(201, 'Success')

        return 400, self.formatter.response(400, 'Failure', info)

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def register_rule(self, data, father_id, user_key):
        text = data['name']

        result, info = self.permission_manager.register_rule(text, father_id, user_key)
        if result:
            return 201, self.formatter.response(201, 'Success')

        return 400, self.formatter.response(400, 'Failure', info)

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def register_event(self, data, father_id, user_key):
        start = data['start']
        end = data['end']
        event_type_id = data['event_type_id']

        result, info = self.permission_manager.register_event(start, end, event_type_id, father_id, user_key)
        if result:
            return 201, self.formatter.response(201, 'Success')

        return 400, self.formatter.response(400, 'Failure', info)

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def remove_notification(self, data, father_id, user_key):
        try:
            notification_id = int(base64.urlsafe_b64decode(data['notification_id']).decode('ascii'))
        except ValueError:
            return 190, self.formatter.response(400, 'Failure', 'Incorrect ID format informed')

        result, info = self.permission_manager.remove_notification(notification_id, father_id, user_key)
        if result is True:
            return 201, self.formatter.response(201, 'Success')

        elif result is None:
            return 404, self.formatter.response(404, 'Failure', info)

        return 400, self.formatter.response(400, 'Failure', info)

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def remove_guest(self, data, father_id, user_key):
        try:
            guest_id = int(base64.urlsafe_b64decode(data['guest_id']).decode('ascii'))
        except ValueError:
            return 190, self.formatter.response(400, 'Failure', 'Incorrect ID format informed')

        result, info = self.permission_manager.remove_guest(guest_id, father_id, user_key)
        if result is True:
            return 201, self.formatter.response(201, 'Success')

        elif result is None:
            return 404, self.formatter.response(404, 'Failure', info)

        return 400, self.formatter.response(400, 'Failure', info)

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def remove_service(self, data, father_id, user_key):
        try:
            service_id = int(base64.urlsafe_b64decode(data['service_id']).decode('ascii'))
        except ValueError:
            return 190, self.formatter.response(400, 'Failure', 'Incorrect ID format informed')

        result, info = self.permission_manager.remove_service(service_id, father_id, user_key)
        if result is True:
            return 201, self.formatter.response(201, 'Success')

        elif result is None:
            return 404, self.formatter.response(404, 'Failure', info)

        return 400, self.formatter.response(400, 'Failure', info)

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def remove_rule(self, data, father_id, user_key):
        try:
            rule_id = int(base64.urlsafe_b64decode(data['rule_id']).decode('ascii'))
        except ValueError:
            return 190, self.formatter.response(400, 'Failure', 'Incorrect ID format informed')

        result, info = self.permission_manager.remove_rule(rule_id, father_id, user_key)
        if result is True:
            return 201, self.formatter.response(201, 'Success')

        elif result is None:
            return 404, self.formatter.response(404, 'Failure', info)

        return 400, self.formatter.response(400, 'Failure', info)

    @runtime_error_decorator
    @key_error_decorator
    @value_error_decorator
    @type_error_decorator
    def remove_event(self, data, father_id, user_key):
        try:
            event_id = int(base64.urlsafe_b64decode(data['event_id']).decode('ascii'))
        except ValueError:
            return 190, self.formatter.response(400, 'Failure', 'Incorrect ID format informed')

        result, info = self.permission_manager.remove_event(event_id, father_id, user_key)
        if result is True:
            return 201, self.formatter.response(201, 'Success')

        elif result is None:
            return 404, self.formatter.response(404, 'Failure', info)

        return 400, self.formatter.response(400, 'Failure', info)

    @runtime_error_decorator
    def drop_session(self, session_key):
        return self.permission_manager.drop_session(session_key)
