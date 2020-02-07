import json
import secrets
import datetime
from functools import wraps
from flask import Flask, request, session, jsonify
from flask_socketio import SocketIO, emit, join_room
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
            del session['room']
            del session['datetime']

        return function(*args)

    return timer_checker


def session_decorator(function):
    @wraps(function)
    def session_checker(*args):
        session_key = session.get('KEY')

        if not session_key:
            return {'message': 'User is not logged or session expired'}, 401

        key = request.get_json()['key']

        if key != session_key:
            return {'message': 'Invalid key'}, 403

        elif key not in keys:
            return {'message': 'Key not recognized'}, 401

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

        except ConnectionRefusedError:
            status_code = 400
            response = {'result': False, 'message': 'User is not logged'}

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


@socket.on('connect')
def verify_connection():
    session_key = session.get('KEY')

    if not session_key:
        raise ConnectionRefusedError

    key = request.get_json()['key']
    if key != session_key:
        raise ConnectionRefusedError

    elif key not in keys:
        raise ConnectionRefusedError


@app.route('/login/<login_type>', methods=['POST'])
@error_decorator
def login(login_type):
    data = request.get_json()
    if login_type == 'resident':
        response, room = formatter.login_resident(data)
        join_room(room + '_resident', request.sid)

    elif login_type == 'employee':
        response, room = formatter.login_employee(data)
        join_room(room + '_employee', request.sid)

    else:
        raise ValueError

    key = secrets.token_urlsafe(10)

    keys.append(key)
    response['key'] = key
    session['KEY'] = key
    session['room'] = room
    session['datetime'] = datetime.datetime.now()

    return response, 201


@app.route('/register/<registration_type>')
@error_decorator
def register(registration_type):
    data = request.get_json()
    if registration_type == 'resident':
        response, room = formatter.register_resident(data)
        join_room(room + '_resident', request.sid)

    elif registration_type == 'employee':
        response, room = formatter.register_employee(data)
        join_room(room + '_employee', request.sid)

    else:
        raise ValueError

    key = secrets.token_urlsafe(10)

    keys.append(key)
    response['key'] = key
    session['KEY'] = key
    session['room'] = room
    session['datetime'] = datetime.datetime.now()

    return response, 201


@app.route('/employee', methods=['GET'])
@session_decorator
@error_decorator
def employee():
    data = request.get_json()
    response = formatter.get_employees(data)

    return response, 200


@app.route('/condominium', methods=['GET'])
@session_decorator
@error_decorator
def condominium():
    data = request.get_json()
    response = formatter.get_condominium(data)

    return response, 200


@app.route('/tower', methods=['GET'])
@session_decorator
@error_decorator
def tower():
    data = request.get_json()
    response = formatter.get_towers(data)

    return response, 200


@app.route('/apartment', methods=['GET'])
@session_decorator
@error_decorator
def apartment():
    data = request.get_json()
    response = formatter.get_apartments(data)

    return response, 200


@app.route('/event', methods=['GET', 'POST', 'DELETE'])
@session_decorator
@error_decorator
def event():
    data = request.get_json()
    if request.method == 'GET':
        response, room = formatter.get_events(data)

    elif request.method == 'POST':
        response, room = formatter.register_event(data)
        emit('event', {'type': 'registration', 'data': data}, room=session['room'] + '_resident')
        emit('event', {'type': 'registration', 'data': data}, room=session['room'] + '_employee')

    else:
        response, room = formatter.remove_event(data)
        emit('event', {'type': 'deletion', 'data': data}, room=session['room'] + '_resident')
        emit('event', {'type': 'deletion', 'data': data}, room=session['room'] + '_employee')

    return response, 204


@app.route('/notification', methods=['GET', 'POST', 'DELETE'])
@session_decorator
@error_decorator
def notification():
    data = request.get_json()
    if request.method == 'GET':
        response = formatter.get_notifications(data)

    elif request.method == 'POST':
        response = formatter.register_notification(data)
        emit('notification', {'type': 'registration', 'data': data}, room=session['room'] + '_resident')
        emit('notification', {'type': 'registration', 'data': data}, room=session['room'] + '_employee')

    else:
        response = formatter.remove_notification(data)
        emit('notification', {'type': 'deletion', 'data': data}, room=session['room'] + '_resident')
        emit('notification', {'type': 'deletion', 'data': data}, room=session['room'] + '_employee')

    return response, 204


@app.route('/guest', methods=['GET', 'POST', 'DELETE'])
@session_decorator
@error_decorator
def guest():
    data = request.get_json()
    if request.method == 'GET':
        response = formatter.get_guests(data)

    elif request.method == 'POST':
        response = formatter.register_guest(data)
        emit('guest', {'type': 'registration', 'data': data}, room=session['room'] + '_employee')

    else:
        response = formatter.remove_guest(data)
        emit('guest', {'type': 'deletion', 'data': data}, room=session['room'] + '_employee')

    return response, 204


@app.route('/service', methods=['GET', 'POST', 'DELETE'])
@session_decorator
@error_decorator
def service():
    data = request.get_json()
    if request.method == 'GET':
        response = formatter.get_services(data)

    elif request.method == 'POST':
        response = formatter.register_service(data)
        emit('service', {'type': 'registration', 'data': data}, room=session['room'] + '_employee')

    else:
        response = formatter.remove_service(data)
        emit('service', {'type': 'deletion', 'data': data}, room=session['room'] + '_employee')

    return response, 204


@app.route('/rule', methods=['GET', 'POST', 'DELETE'])
@session_decorator
@error_decorator
def rule():
    data = request.get_json()
    if request.method == 'GET':
        response = formatter.get_rules(data)

    elif request.method == 'POST':
        response = formatter.register_rule(data)
        emit('rule', {'type': 'registration', 'data': data}, room=session['room'] + '_resident')
        emit('rule', {'type': 'registration', 'data': data}, room=session['room'] + '_employee')

    else:
        response = formatter.remove_rule(data)
        emit('rule', {'type': 'deletion', 'data': data}, room=session['room'] + '_resident')
        emit('rule', {'type': 'deletion', 'data': data}, room=session['room'] + '_employee')

    return response, 204


if __name__ == '__main__':
    import database_cleaner
    from controller.formatter import JSONFormatter

    formatter = JSONFormatter()
    socket.run(app)
