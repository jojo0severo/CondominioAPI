import json
import secrets
import datetime
from functools import wraps
from flask import Flask, request, session, jsonify
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = secrets.token_urlsafe(10)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/api.db'

db = SQLAlchemy(app)
socket = SocketIO(app)
keys = []


def timer_decorator(function):
    @wraps(function)
    def timer_checker(*args):
        datetime_diff = session['datetime'] - datetime.datetime.now()
        if datetime_diff.days >= 2:
            formatter.drop_session(session['type'], session['KEY'])
            del session['KEY']
            del session['datetime']

        return function(*args)

    return timer_checker


def session_decorator(function):
    @wraps(function)
    def session_checker(*args):
        key = request.get_json()['key']
        session_key = session.get('KEY')

        if not session_key:
            return {'message': 'User is not logged or session expired'}, 401

        elif key not in keys:
            return {'message': 'Key not recognized'}, 401

        elif key != session_key:
            return {'message': 'Corrupted key'}, 403

        else:
            return function(*args)

    return session_checker


def error_decorator(function):
    @wraps(function)
    def error_handler(*args):
        try:
            response, status_code = function(*args)

        except json.JSONDecodeError:
            status_code = 415
            response = {'result': False, 'message': 'Wrong message format'}

        except ReferenceError:
            status_code = 400
            response = {'result': False, 'message': 'Data could not be found'}

        except PermissionError:
            status_code = 402
            response = {'result': False, 'message': 'User do not have the privileges to do such operation'}

        except ValueError:
            status_code = 400
            response = {'result': False, 'message': 'Invalid/Wrong information sent to request'}

        except NotImplementedError:
            status_code = 402
            response = {'result': False, 'message': 'Endpoint can not send the information'}

        except KeyError:
            status_code = 400
            response = {'result': False, 'message': 'Wrong keys sent'}

        except TypeError:
            status_code = 400
            response = {'result': False, 'message': 'Wrong values type sent'}

        except RuntimeError:
            status_code = 500
            response = {'result': False, 'message': 'Something went wrong with the application'}

        except Exception as e:
            status_code = 500
            response = {'result': False, 'message': 'Unknown error -> ' + str(e)}

        return jsonify(response), status_code

    return error_handler


@app.before_request
def session_configuration():
    session.permanent = True
    session.modified = True
    app.permanent_session_lifetime = datetime.timedelta(days=365)


@app.route('/login/resident', methods=['POST'])
@error_decorator
def login_resident():
    data = request.get_json()
    response = formatter.login_resident(data)

    key = secrets.token_urlsafe(10)

    keys.append(key)
    response['key'] = key
    session['KEY'] = key
    session['datetime'] = datetime.datetime.now()

    return response, 201


@app.route('/login/employee', methods=['POST'])
@error_decorator
def login_employee():
    data = request.get_json()
    response = formatter.login_employee(data)

    key = secrets.token_urlsafe(10)

    keys.append(key)
    response['key'] = key
    session['KEY'] = key
    session['datetime'] = datetime.datetime.now()

    return response, 201


@app.route('/employee', methods=['GET', 'POST', 'PUT', 'DELETE'])
@error_decorator
@session_decorator
@timer_decorator
def employee():
    data = request.get_json()
    if request.method == 'GET':
        response = formatter.get_employee(session.get('USER'), data)
        status_code = 200

    elif request.method == 'POST':
        response = formatter.register_employee(session.get('USER'), data)
        status_code = 201

    elif request.method == 'PUT':
        response = formatter.edit_employee(session.get('USER'), data)
        status_code = 205

    else:
        response = formatter.delete_employee(session.get('USER'), data)
        status_code = 205

    return response, status_code


@app.route('/resident', methods=['GET', 'POST', 'PUT', 'DELETE'])
@error_decorator
@session_decorator
@timer_decorator
def resident():
    data = request.get_json()
    if request.method == 'GET':
        response = formatter.get_resident(session.get('USER'), data)
        status_code = 200

    elif request.method == 'POST':
        response = formatter.register_resident(session.get('USER'), data)
        status_code = 201

    elif request.method == 'PUT':
        response = formatter.edit_resident(session.get('USER'), data)
        status_code = 205

    else:
        response = formatter.delete_resident(session.get('USER'), data)
        status_code = 205

    return response, status_code


@app.route('/apartment/all', methods=['GET'])
@error_decorator
@session_decorator
@timer_decorator
def all_apartments():
    data = request.get_json()
    response = formatter.get_all_apartment(data)

    return response, 200


@app.route('/apartment', methods=['GET', 'POST', 'PUT', 'DELETE'])
@error_decorator
@session_decorator
@timer_decorator
def apartment():
    data = request.get_json()

    if request.method == 'GET':
        response = formatter.get_apartment(data)
        status_code = 200

    elif request.method == 'POST':
        response = formatter.register_apartment(data)
        status_code = 201

    elif request.method == 'PUT':
        response = formatter.edit_apartment(data)
        status_code = 205

    else:
        response = formatter.delete_apartment(data)
        status_code = 205

    return response, status_code


@app.route('/tower/all', methods=['GET'])
@error_decorator
@session_decorator
@timer_decorator
def all_towers():
    data = request.get_json()
    response = formatter.get_all_tower(data)

    return response, 200


@app.route('/tower', methods=['GET', 'POST', 'PUT', 'DELETE'])
@error_decorator
@session_decorator
@timer_decorator
def tower():
    data = request.get_json()

    if request.method == 'GET':
        response = formatter.get_tower(data)
        status_code = 200

    elif request.method == 'POST':
        response = formatter.register_tower(data)
        status_code = 201

    elif request.method == 'PUT':
        response = formatter.edit_tower(data)
        status_code = 205

    else:
        response = formatter.remove_tower(data)
        status_code = 205

    return response, status_code


@app.route('/event/all', methods=['GET'])
@error_decorator
@session_decorator
@timer_decorator
def all_events():
    data = request.get_json()
    response = formatter.get_all_event(data)

    return response, 200


@app.route('/event', methods=['GET', 'POST', 'PUT', 'DELETE'])
@error_decorator
@session_decorator
@timer_decorator
def event():
    data = request.get_json()

    if request.method == 'GET':
        response = formatter.get_event(data)
        status_code = 200

    elif request.method == 'POST':
        response = formatter.register_event(data)
        status_code = 201

    elif request.method == 'PUT':
        response = formatter.edit_event(data)
        status_code = 205

    else:
        response = formatter.remove_event(data)
        status_code = 205

    return response, status_code


@app.route('/complex_event/all', methods=['GET'])
@error_decorator
@session_decorator
@timer_decorator
def all_complex_events():
    data = request.get_json()
    response = formatter.get_all_complex_event(data)

    return response, 200


@app.route('/complex_event', methods=['GET', 'POST', 'PUT', 'DELETE'])
@error_decorator
@session_decorator
@timer_decorator
def complex_event():
    data = request.get_json()

    if request.method == 'GET':
        response = formatter.get_complex_event(data)
        status_code = 200

    elif request.method == 'POST':
        response = formatter.register_complex_event(data)
        status_code = 201

    elif request.method == 'PUT':
        response = formatter.edit_complex_event(data)
        status_code = 205

    else:
        response = formatter.delete_complex_event(data)
        status_code = 205

    return response, status_code


@app.route('/resident_event/all', methods=['GET'])
@error_decorator
@session_decorator
def all_resident_events():
    data = request.get_json()
    response = formatter.get_all_resident_event(data)

    return response, 200


@app.route('/resident_event', methods=['GET', 'POST', 'PUT', 'DELETE'])
@error_decorator
@session_decorator
def resident_event():
    data = request.get_json()

    if request.method == 'GET':
        response = formatter.get_resident_event(data)
        status_code = 200

    elif request.method == 'POST':
        response = formatter.register_resident_event(data)
        status_code = 201

    elif request.method == 'PUT':
        response = formatter.edit_resident_event(data)
        status_code = 205

    else:
        response = formatter.delete_resident_event(data)
        status_code = 205

    return response, status_code


@app.route('/warning/all', methods=['GET'])
@error_decorator
@session_decorator
def all_warnings():
    data = request.get_json()
    response = formatter.get_all_warning(data)

    return response, 200


@app.route('/warning', methods=['GET', 'POST', 'PUT', 'DELETE'])
@error_decorator
@session_decorator
def warning():
    data = request.get_json()

    if request.method == 'GET':
        response = formatter.get_warning(data)
        status_code = 200

    elif request.method == 'POST':
        response = formatter.register_warning(data)
        status_code = 201

    elif request.method == 'PUT':
        response = formatter.edit_warning(data)
        status_code = 205

    else:
        response = formatter.delete_warning(data)
        status_code = 205

    return response, status_code


@app.route('/rule/all', methods=['GET'])
@error_decorator
@session_decorator
def all_rules():
    data = request.get_json()
    response = formatter.get_all_rule(data)

    return response, 200


@app.route('/rule', methods=['GET', 'POST', 'PUT', 'DELETE'])
@error_decorator
@session_decorator
def rule():
    data = request.get_json()

    if request.method == 'GET':
        response = formatter.get_rule(data)
        status_code = 200

    elif request.method == 'POST':
        response = formatter.register_rule(data)
        status_code = 201

    elif request.method == 'PUT':
        response = formatter.edit_rule(data)
        status_code = 205

    else:
        response = formatter.delete_rule(data)
        status_code = 205

    return response, status_code


@app.route('/shop/all', methods=['GET'])
@error_decorator
@session_decorator
def all_shops():
    data = request.get_json()
    response = formatter.get_all_shop(data)

    return response, 200


@app.route('/shop', methods=['GET', 'POST', 'PUT', 'DELETE'])
@error_decorator
@session_decorator
def shop():
    data = request.get_json()

    if request.method == 'GET':
        response = formatter.get_shop(data)
        status_code = 200

    elif request.method == 'POST':
        response = formatter.register_shop(data)
        status_code = 201

    elif request.method == 'PUT':
        response = formatter.edit_shop(data)
        status_code = 205

    else:
        response = formatter.delete_shop(data)
        status_code = 205

    return response, status_code


@app.route('/<shop>/item/all', methods=['GET'])
@error_decorator
@session_decorator
def all_items(shop_name):
    data = request.get_json()
    response = formatter.get_all_item(shop_name, data)

    return response, 200


@app.route('/<shop>/item', methods=['GET', 'POST', 'PUT', 'DELETE'])
@error_decorator
@session_decorator
def item(shop_name):
    data = request.get_json()

    if request.method == 'GET':
        response = formatter.get_item(shop_name, data)
        status_code = 200

    elif request.method == 'POST':
        response = formatter.register_item(shop_name, data)
        status_code = 201

    elif request.method == 'PUT':
        response = formatter.edit_item(shop_name, data)
        status_code = 205

    else:
        response = formatter.delete_item(shop_name, data)
        status_code = 205

    return response, status_code


@app.route('/service/all', methods=['GET'])
@error_decorator
@session_decorator
def all_services():
    data = request.get_json()
    response = formatter.get_all_service(data)

    return response, 200


@app.route('/service', methods=['GET', 'POST', 'PUT', 'DELETE'])
@error_decorator
@session_decorator
def service():
    data = request.get_json()

    if request.method == 'GET':
        response = formatter.get_service(data)
        status_code = 200

    elif request.method == 'POST':
        response = formatter.register_service(data)
        status_code = 201

    elif request.method == 'PUT':
        response = formatter.edit_service(data)
        status_code = 205

    else:
        response = formatter.delete_service(data)
        status_code = 205

    return response, status_code


@app.route('/service_day/all', methods=['GET'])
@error_decorator
@session_decorator
def all_service_days():
    data = request.get_json()
    response = formatter.get_all_service_day(data)

    return response, 200


@app.route('/service_day', methods=['GET', 'POST', 'PUT', 'DELETE'])
@error_decorator
@session_decorator
def service_day():
    data = request.get_json()

    if request.method == 'GET':
        response = formatter.get_service_day(data)
        status_code = 200

    elif request.method == 'POST':
        response = formatter.register_service_day(data)
        status_code = 201

    elif request.method == 'PUT':
        response = formatter.edit_service_day(data)
        status_code = 205

    else:
        response = formatter.delete_service_day(data)
        status_code = 205

    return response, status_code


if __name__ == '__main__':
    from controller.formatter import JSONFormatter

    formatter = JSONFormatter()

    import database_cleaner

    socket.run(app)
