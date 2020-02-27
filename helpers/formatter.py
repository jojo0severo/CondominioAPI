import base64


class JSONFormatter:

    def format_super_user_connection(self, result, info, status):
        if result:
            return status['success'], {'status': status['success'], 'result': True, 'event': 'Success', 'message': '', 'data': {'username': info.username}}

        return status['failure'],  {'status': status['failure'], 'result': False, 'event': 'Failure', 'message': 'Super user could not be logged', 'data': {}}

    def format_resident_login(self, result, info, status):
        if result:
            if not info:
                return status['empty'], {'status': status['empty'], 'result': False, 'event': 'Empty', 'message': 'No resident found', 'data': []}

            response = {'status': status['success'],
                        'result': True,
                        'event': 'Success',
                        'message': '',
                        'data': []}

            for resident in info:
                response['data'].append(self.format_resident(resident))

            return status['success'], response

        return status['failure'], {'status': status['failure'], 'result': False, 'event': 'Failure', 'message': info, 'data': {}}

    def format_resident_connection(self, result, info, status):
        if result:
            return {'status': status['success'],
                    'result': True,
                    'event': 'Success',
                    'message': '',
                    'data': {
                        'resident': self.format_resident(info[0]),
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

    def format_guests(self, result, info, status):
        if result:
            if not info:
                return {'status': status['empty'], 'result': False, 'event': 'Empty', 'message': 'No guest found', 'data': []}

            response = {'status': status['success'], 'result': True, 'event': 'Success', 'message': '', 'data': []}
            for guest in info:
                response['data'].append(self.format_guest(guest))

            return response

        return {'status': status['failure'], 'result': False, 'event': 'Failure', 'message': info, 'data': {}}

    def format_services(self, result, info, status):
        if result:
            if not info:
                return {'status': status['empty'], 'result': False, 'event': 'Empty', 'message': 'No service found',
                        'data': []}

            response = {'status': status['success'], 'result': True, 'event': 'Success', 'message': '', 'data': []}
            for service in info:
                response['data'].append(self.format_service(service))

            return response

        return {'status': status['failure'], 'result': False, 'event': 'Failure', 'message': info, 'data': {}}

    def format_rules(self, result, info, status):
        if result:
            if not info:
                return {'status': status['empty'], 'result': False, 'event': 'Empty', 'message': 'No rule found',
                        'data': []}

            response = {'status': status['success'], 'result': True, 'event': 'Success', 'message': '', 'data': []}
            for rule in info:
                response['data'].append({'rule': self.format_rule(rule), 'author': self.format_employee(rule.author)})

            return response

        return {'status': status['failure'], 'result': False, 'event': 'Failure', 'message': info, 'data': {}}

    def format_events(self, result, info, status):
        if result:
            if not info:
                return {'status': status['empty'], 'result': False, 'event': 'Empty', 'message': 'No event found',
                        'data': []}

            response = {'status': status['success'], 'result': True, 'event': 'Success', 'message': '', 'data': []}
            for event in info:
                response['data'].append(self.format_event(event))

            return response

        return {'status': status['failure'], 'result': False, 'event': 'Failure', 'message': info, 'data': {}}

    @staticmethod
    def response(status, event, message=''):
        return {'status': status, 'result': status in [200, 201], 'event': event, 'message': message}

    @staticmethod
    def format_resident(resident):
        return {'ID': base64.urlsafe_b64encode(str(resident.id).encode('ascii')).decode('ascii'),
                'CPF': resident.cpf,
                'Name': resident.name,
                'Birthday': resident.birthday.strftime('%Y-%m-%d'),
                'PhotoLocation': resident.photo_location}

    @staticmethod
    def format_employee(employee):
        return {'ID': base64.urlsafe_b64encode(str(employee.id).encode('ascii')).decode('ascii'),
                'CPF': employee.cpf,
                'Name': employee.name,
                'Birthday': employee.birthday.strftime('%Y-%m-%d'),
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

    @staticmethod
    def format_guest(guest):
        return {'Name': guest.name,
                'Arrival': guest.arrival}

    @staticmethod
    def format_service(service):
        return {'ServiceName': service.name,
                'EmployeeName': service.employee,
                'Arrival': service.arrival.strftime('%Y-%m-%d %H:%M')}

    @staticmethod
    def format_rule(rule):
        return {'Text': rule.text}

    @staticmethod
    def format_event(event):
        return {'Name': event.event_type.name,
                'Start': event.start_datetime,
                'End': event.end_datetime}
