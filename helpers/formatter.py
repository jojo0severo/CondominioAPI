import base64


class JSONFormatter:

    def format_super_user_connection(self, result, info, status):
        if result:
            return status['success'], {'status': status['success'], 'result': True, 'event': 'Success', 'message': '', 'data': {'username': info.username}}

        return status['failure'],  {'status': status['failure'], 'result': False, 'event': 'Failure', 'message': 'Super user could not be logged', 'data': {}}

    def format_resident_login(self, result, info, status):
        if result:
            if not info:
                return status['empty'], {'status': status['empty'], 'result': False, 'event': 'Empty', 'message': 'No resident found', 'data': []}, None, None

            response = {'status': status['success'],
                        'result': True,
                        'event': 'Success',
                        'message': '',
                        'data': []}

            for resident in info:
                response['data'].append(self.format_resident(resident))

            return status['success'], response, None, None

        return status['failure'], {'status': status['failure'], 'result': False, 'event': 'Failure', 'message': info, 'data': {}}, None, None

    def format_resident_connection(self, result, info, status):
        if result:
            return {'status': status['success'],
                    'result': True,
                    'event': 'Success',
                    'message': '',
                    'data': {
                        'resident': self.format_employee(info[0]),
                        'apartment': self.format_apartment(info[1]),
                        'tower': self.format_tower(info[2]),
                        'condominium': self.format_condominium(info[3]),
                        'address': self.format_address(info[4])
                    }
                    }

        return {'status': status['failure'], 'result': False, 'event': 'Failure', 'message': info, 'data': {}}

    def format_employee_connection(self, result, info, status):
        if result:
            return {'status': status['success'],
                    'result': True,
                    'event': 'Success',
                    'message': '',
                    'data': {
                        'employee': self.format_employee(info[0]),
                        'condominium': self.format_condominium(info[1]),
                        'address': self.format_address(info[2])
                    }
                    }, info[1].name, info[0].id

        return {'status': status['failure'], 'result': False, 'event': 'Failure', 'message': info, 'data': {}}, None, None

    def format_employees(self, result, info, status):
        if result:
            if not info:
                return {'status': status['empty'], 'result': False, 'event': 'Empty', 'message': 'No employee found', 'data': []}

            response = {'status': status['success'], 'result': True, 'event': 'Success', 'message': '', 'data': []}
            for employee in info:
                response['data'].append(self.format_employee(employee))
            return response

        return {'status': status['failure'], 'result': False, 'event': 'Failure', 'message': info, 'data': {}}

    def format_residents(self, result, info, status):
        if result:
            if not info:
                return {'status': status['empty'], 'result': False, 'event': 'Empty', 'message': 'No resident found', 'data': []}

            response = {'status': status['success'], 'result': True, 'event': 'Success', 'message': '', 'data': []}
            for resident in info:
                response['data'].append(self.format_resident(resident))
            return response

        return {'status': status['failure'], 'result': False, 'event': 'Failure', 'message': info, 'data': {}}

    def format_notifications(self, result, info, status):
        if result:
            if not info:
                return {'status': status['empty'], 'result': False, 'event': 'Empty', 'message': 'No notification found', 'data': []}

            response = {'status': status['success'], 'result': True, 'event': 'Success', 'message': '', 'data': []}
            for notification in info:
                response['data'].append(self.format_notification(notification))

            return response

        return {'status': status['failure'], 'result': False, 'event': 'Failure', 'message': info, 'data': {}}

    @staticmethod
    def response(status, event, message=''):
        return {'status': status, 'result': status in [200, 201], 'event': event, 'message': message}

    @staticmethod
    def format_resident(resident):
        return {'id': base64.urlsafe_b64encode(str(resident.id).encode('ascii')).decode('ascii'),
                'CPF': resident.cpf,
                'Name': resident.name,
                'Birthday': resident.birthday.strftime("%Y-%m-%d"),
                'PhotoLocation': resident.photo_location}

    @staticmethod
    def format_employee(employee):
        return {'id': base64.urlsafe_b64encode(str(employee.id).encode('ascii')).decode('ascii'),
                'CPF': employee.cpf,
                'Name': employee.name,
                'Birthday': employee.birthday.strftime("%Y-%m-%d"),
                'Role': employee.role,
                'PhotoLocation': employee.photo_location}

    @staticmethod
    def format_apartment(apartment):
        return {'Number': apartment.apt_number}

    @staticmethod
    def format_tower(tower):
        return {'Name': tower.name}

    @staticmethod
    def format_condominium(condominium):
        return {'Name': condominium.name,
                'PhotoLocation': condominium.photo_location}

    @staticmethod
    def format_address(address):
        return {'Street': address.street_name,
                'Neighbourhood': address.neighbourhood,
                'City': address.city.name}

    @staticmethod
    def format_notification(notification):
        return {'Type': notification.type,
                'Title': notification.title,
                'Finish Date': notification.finish_date}
