import base64


class JSONFormatter:
    def format_resident_connection(self, result, info, status):
        if result:
            condominium = self.format_condominium(info[3])

            return {'status': status['success'],
                    'result': True,
                    'event': 'Resident successfully logged',
                    'data': {
                        'resident': self.format_resident(info[0]),
                        'apartment': self.format_apartment(info[1]),
                        'tower': self.format_tower(info[2]),
                        'condominium': condominium,
                        'address': self.format_address(info[4])
                    }
                    }, condominium['Name']

        return {'status': status['failure'], 'result': False, 'event': info, 'data': {}}, None

    def format_employee_connection(self, result, info, status):
        if result:
            condominium = self.format_condominium(info[1])
            return {'status': status['success'],
                    'result': True,
                    'event': 'Resident successfully logged',
                    'data': {
                        'employee': self.format_employee(info[0]),
                        'condominium': condominium,
                        'address': self.format_address(info[2])
                    }
                    }, condominium['Name']

        return {'status': status['failure'], 'result': False, 'event': info, 'data': {}}, None

    def format_employees(self, result, info, status):
        if result:
            if not info:
                return {'status': status['empty'], 'result': False, 'event': 'No employee found', 'data': []}

            response = {'status': status['success'], 'result': True, 'event': 'Employees recovered', 'data': []}
            for employee in info:
                response['data'].append(self.format_employee(employee))
            return response

        return {'status': status['failure'], 'result': False, 'event': info, 'data': {}}

    def format_residents(self, result, info, status):
        if result:
            if not info:
                return {'status': 404, 'result': False, 'event': 'No resident found', 'data': []}

            response = {'status': status['success'], 'result': True, 'event': 'Residents recovered', 'data': []}
            for resident in info:
                response['data'].append(self.format_resident(resident))
            return response

        return {'status': status['failure'], 'result': False, 'event': info, 'data': {}}

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
