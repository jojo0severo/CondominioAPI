import json
import secrets
from functools import wraps
from flask import Flask, request, session
from flask_socketio import SocketIO
from model.database import db_location, setup_database

setup_database()

format = '%Y-%m-%d %H:%M:%S'

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = secrets.token_urlsafe(10)
app.config['SQLALCHEMY_DATABASE_URI'] = db_location

socket = SocketIO(app)


def session_decorator(function):
    @wraps(function)
    def session_checker(*args):
        if not session.get('USERNAME'):
            return 'User is not logged', 403
        else:
            return function(*args)

    return session_checker


def error_decorator(function):
    @wraps(function)
    def error_handler(*args):
        response = {'message': ''}

        try:
            message, status_code = function(*args)
            response['message'] = message

        except json.JSONDecodeError:
            status_code = 415
            response['message'] = 'Wrong message format'

        except KeyError:
            status_code = 400
            response['message'] = 'Wrong keys sent'

        except TypeError:
            status_code = 400
            response['message'] = 'Wrong values type sent'

        except Exception as e:
            status_code = 500
            response['message'] = 'Unknown error -> ' + str(e)

        return response, status_code

    return error_handler


@app.route('/login', methods=['POST'])
@error_decorator
def login():
    message = 'User logged'
    status_code = 201

    info = request.get_json()

    session['USERNAME'] = info['username']

    return message, status_code


@app.route('/employee/all', methods=['GET'])
@error_decorator
@session_decorator
def get_all_employees():
    message = 'Employees recovered'
    status_code = 200

    info = request.get_json()

    return message, status_code


@app.route('/employee', methods=['GET'])
@error_decorator
@session_decorator
def get_one_employee():
    message = 'Employee recovered'
    status_code = 200

    info = request.get_json()

    return message, status_code


@app.route('/employee', methods=['POST'])
@error_decorator
@session_decorator
def post_employee():
    message = 'Employee registered'
    status_code = 201

    info = request.get_json()

    return message, status_code


@app.route('/employee', methods=['PUT'])
@error_decorator
@session_decorator
def put_employee():
    message = 'Employee updated'
    status_code = 205

    info = request.get_json()

    return message, status_code


@app.route('/employee', methods=['DELETE'])
@error_decorator
@session_decorator
def delete_employee():
    message = 'Employee deleted'
    status_code = 205

    info = request.get_json()

    return message, status_code


@app.route('/user/all', methods=['GET'])
@error_decorator
@session_decorator
def get_all_users():
    message = 'Users recovered'
    status_code = 200

    info = request.get_json()

    return message, status_code


@app.route('/user', methods=['GET'])
@error_decorator
@session_decorator
def get_one_user():
    message = 'User recovered'
    status_code = 200

    info = request.get_json()

    return message, status_code


@app.route('/user', methods=['POST'])
@error_decorator
@session_decorator
def post_user():
    message = 'User registered'
    status_code = 201

    info = request.get_json()

    return message, status_code


@app.route('/user', methods=['PUT'])
@error_decorator
@session_decorator
def put_user():
    message = 'User updated'
    status_code = 205

    info = request.get_json()

    return message, status_code


@app.route('/user', methods=['DELETE'])
@error_decorator
@session_decorator
def delete_user():
    message = 'User deleted'
    status_code = 205

    info = request.get_json()

    return message, status_code


@app.route('/tower/all', methods=['GET'])
@error_decorator
@session_decorator
def get_all_towers():
    message = 'Towers recovered'
    status_code = 200

    info = request.get_json()

    return message, status_code


@app.route('/tower', methods=['GET'])
@error_decorator
@session_decorator
def get_one_tower():
    message = 'Tower recovered'
    status_code = 200

    info = request.get_json()

    return message, status_code


@app.route('/tower', methods=['POST'])
@error_decorator
@session_decorator
def post_tower():
    message = 'Tower registered'
    status_code = 201

    info = request.get_json()

    return message, status_code


@app.route('/tower', methods=['DELETE'])
@error_decorator
@session_decorator
def delete_tower():
    message = 'Tower deleted'
    status_code = 205

    info = request.get_json()

    return message, status_code


@app.route('/complex/all', methods=['GET'])
@error_decorator
@session_decorator
def get_all_complexes():
    message = 'Complexes recovered'
    status_code = 200

    info = request.get_json()

    return message, status_code


@app.route('/complex', methods=['GET'])
@error_decorator
@session_decorator
def get_one_complex():
    message = 'Complex recovered'
    status_code = 200

    info = request.get_json()

    return message, status_code


@app.route('/complex', methods=['POST'])
@error_decorator
@session_decorator
def post_complex():
    message = 'Complex registered'
    status_code = 201

    info = request.get_json()

    return message, status_code


@app.route('/complex', methods=['DELETE'])
@error_decorator
@session_decorator
def delete_complex():
    message = 'Complex deleted'
    status_code = 205

    info = request.get_json()

    return message, status_code


@app.route('/event/all', methods=['GET'])
@error_decorator
@session_decorator
def get_all_events():
    message = 'Events recovered'
    status_code = 200

    info = request.get_json()

    return message, status_code


@app.route('/event', methods=['GET'])
@error_decorator
@session_decorator
def get_one_event():
    message = 'Event recovered'
    status_code = 200

    info = request.get_json()

    return message, status_code


@app.route('/event', methods=['POST'])
@error_decorator
@session_decorator
def post_event():
    message = 'Event registered'
    status_code = 201

    info = request.get_json()

    return message, status_code


@app.route('/event', methods=['DELETE'])
@error_decorator
@session_decorator
def delete_event():
    message = 'Event deleted'
    status_code = 205

    info = request.get_json()

    return message, status_code


@app.route('/warning/all', methods=['GET'])
@error_decorator
@session_decorator
def get_all_warnings():
    message = 'Warnings recovered'
    status_code = 200

    info = request.get_json()

    return message, status_code


@app.route('/warning', methods=['GET'])
@error_decorator
@session_decorator
def get_one_warning():
    message = 'Warning recovered'
    status_code = 200

    info = request.get_json()

    return message, status_code


@app.route('/warning', methods=['POST'])
@error_decorator
@session_decorator
def post_warning():
    message = 'Warning registered'
    status_code = 201

    info = request.get_json()

    return message, status_code


@app.route('/warning', methods=['DELETE'])
@error_decorator
@session_decorator
def delete_warning():
    message = 'Warning deleted'
    status_code = 205

    info = request.get_json()

    return message, status_code


@app.route('/rule/all', methods=['GET'])
@error_decorator
@session_decorator
def get_all_rules():
    message = 'Rules recovered'
    status_code = 200

    info = request.get_json()

    return message, status_code


@app.route('/rule', methods=['GET'])
@error_decorator
@session_decorator
def get_one_rule():
    message = 'Rule recovered'
    status_code = 200

    info = request.get_json()

    return message, status_code


@app.route('/rule', methods=['POST'])
@error_decorator
@session_decorator
def post_rule():
    message = 'Rule registered'
    status_code = 201

    info = request.get_json()

    return message, status_code


@app.route('/rule', methods=['DELETE'])
@error_decorator
@session_decorator
def delete_rule():
    message = 'Rule deleted'
    status_code = 205

    info = request.get_json()

    return message, status_code


@app.route('/shop/all', methods=['GET'])
@error_decorator
@session_decorator
def get_all_shops():
    message = 'Shops recovered'
    status_code = 200

    info = request.get_json()

    return message, status_code


@app.route('/shop', methods=['GET'])
@error_decorator
@session_decorator
def get_one_shop():
    message = 'Shop recovered'
    status_code = 200

    info = request.get_json()

    return message, status_code


@app.route('/shop', methods=['POST'])
@error_decorator
@session_decorator
def post_shop():
    message = 'Shop registered'
    status_code = 201

    info = request.get_json()

    return message, status_code


@app.route('/shop', methods=['DELETE'])
@error_decorator
@session_decorator
def delete_shop():
    message = 'Shop deleted'
    status_code = 205

    info = request.get_json()

    return message, status_code


@app.route('/<shop>/items/all', methods=['GET'])
@error_decorator
@session_decorator
def get_all_items(shop):
    message = 'Items recovered'
    status_code = 200

    info = request.get_json()

    return message, status_code


@app.route('/<shop>/items', methods=['GET'])
@error_decorator
@session_decorator
def get_one_item(shop):
    message = 'Item recovered'
    status_code = 200

    info = request.get_json()

    return message, status_code


@app.route('/<shop>/items', methods=['POST'])
@error_decorator
@session_decorator
def post_item(shop):
    message = 'Item registered'
    status_code = 201

    info = request.get_json()

    return message, status_code


@app.route('/<shop>/items', methods=['DELETE'])
@error_decorator
@session_decorator
def delete_item(shop):
    message = 'Item deleted'
    status_code = 205

    info = request.get_json()

    return message, status_code


if __name__ == '__main__':
    socket.run(app)
