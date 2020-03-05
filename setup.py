from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import AuthenticationBackend, AuthenticationError, SimpleUser, UnauthenticatedUser, AuthCredentials
from starlette.middleware import Middleware
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from sqlalchemy.ext.declarative import declarative_base
import databases
import secrets
from functools import wraps
import datetime
import time
import json
import os

Base = declarative_base()
db = databases.Database(os.environ['DATABASE_URL'])

keys = set()
blocked_sessions = set()

super_user_url = 'secret'
print('\n', '===', super_user_url, '===', '\n')

handler = None


def set_handler():
    global handler

    if handler is None:
        from helpers.handler import Handler

        handler = Handler()


async def login_super_user(request):
    set_handler()

    before = time.time()
    try:
        data = await request.json()

        status, response, id_, db_time = await handler.login_super_user(data)

        if status == 200:
            key = secrets.token_urlsafe(20)

            keys.add(key)
            response['key'] = key

            handler.register_key('super_user', key)

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    after = time.time()
    response['time'] = after - before
    response['db_time'] = db_time

    return JSONResponse(response, status_code=status)


async def register_condominium_super_user(request):
    before = time.time()

    try:
        condominium_schema = request.get_json(force=True)['schema']
        status, response = handler.build_condominium_schema(condominium_schema)

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    after = time.time()
    response['time'] = after - before

    return JSONResponse(response, status_code=status)


async def login(request):
    before = time.time()

    login_type = str(request.path_params['login_type']).lower()

    try:
        data = request.get_json(force=True)
        if login_type == 'resident':
            status, response, room, id_ = handler.login_resident(data)

            if status == 200 or (status == 404 and login_type == 'resident'):

                key = secrets.token_urlsafe(20)

                keys.add(key)
                response['key'] = key

                handler.register_key(login_type, key)

        elif login_type == 'employee':
            status, response, room, id_, login_type = handler.login_employee(data)

            if status == 200:
                key = secrets.token_urlsafe(20)

                keys.add(key)
                response['key'] = key

                handler.register_key(login_type, key)

        else:
            status = 404
            response = {'status': 404, 'result': False, 'event': 'Unknown login type', 'data': {}}

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    after = time.time()
    response['time'] = after - before

    return JSONResponse(response, status_code=status)


async def register(request):
    before = time.time()

    registration_type = str(request.path_params['registration_type']).lower()
    try:
        data = request.get_json(force=True)
        if registration_type == 'user':
            status, response = handler.register_resident_user(data)

        elif registration_type == 'resident':
            status, response = handler.register_resident(data)

        elif registration_type == 'employee':
            status, response = handler.register_employee(data)

        else:
            status = 400
            response = {'status': 400, 'result': False, 'event': 'Invalid registration type', 'data': {}}

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    after = time.time()
    response['time'] = after - before

    return JSONResponse(response, status_code=status)


async def employees():
    before = time.time()

    try:
        status, response = handler.get_employees(session['ID'], session['KEY'])

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    after = time.time()
    response['time'] = after - before

    return JSONResponse(response, status_code=status)


async def residents(request):
    before = time.time()

    try:
        data = request.get_json(force=True)
        status, response = handler.get_residents(data, session['ID'], session['KEY'])

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    after = time.time()
    response['time'] = after - before

    return JSONResponse(response, status_code=status)


async def notification(request):
    before = time.time()

    data = request.get_json(force=True)
    if request.method == 'GET':
        status, response = handler.get_notifications(session['ID'], session['KEY'])

        if status == 190:
            status = 400
            blocked_sessions.add(session['KEY'])

    elif request.method == 'POST':
        status, response = handler.register_notification(data, session['ID'], session['KEY'])

    else:
        status, response = handler.remove_notification(data, session['ID'], session['KEY'])

    after = time.time()
    response['time'] = after - before

    return JSONResponse(response, status_code=status)


async def guest(request):
    before = time.time()

    data = request.get_json(force=True)
    if request.method == 'GET':
        status, response = handler.get_guests(data, session['ID'], session['KEY'])

    elif request.method == 'POST':
        status, response = handler.register_guest(data, session['ID'], session['KEY'])

    else:
        status, response = handler.remove_guest(data, session['ID'], session['KEY'])

    after = time.time()
    response['time'] = after - before

    return JSONResponse(response, status_code=status)


async def service(request):
    before = time.time()

    data = request.get_json(force=True)
    if request.method == 'GET':
        response = handler.get_services(session['ID'], session['KEY'])

    elif request.method == 'POST':
        response = handler.register_service(data, session['ID'], session['KEY'])

    else:
        response = handler.remove_service(data, session['ID'], session['KEY'])

    after = time.time()
    response['time'] = after - before

    return JSONResponse(response, status_code=204)


async def rule(request):
    before = time.time()

    data = request.get_json(force=True)
    if request.method == 'GET':
        response = handler.get_rules(session['ID'], session['KEY'])

    elif request.method == 'POST':
        response = handler.register_rule(data, session['ID'], session['KEY'])

    else:
        response = handler.remove_rule(data, session['ID'], session['KEY'])

    after = time.time()
    response['time'] = after - before

    return JSONResponse(response, status_code=204)


async def event_type():
    before = time.time()

    try:
        status, response = handler.get_event_types(session['ID'], session['KEY'])

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    after = time.time()
    response['time'] = after - before

    return JSONResponse(response, status_code=status)


async def event(request):
    before = time.time()

    try:
        data = request.get_json(force=True)
        if request.method == 'GET':
            status, response = handler.get_events(data, session['ID'], session['KEY'])

        elif request.method == 'POST':
            status, response = handler.register_event(data, session['ID'], session['KEY'])

        else:
            status, response = handler.remove_event(data, session['ID'], session['KEY'])

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    after = time.time()
    response['time'] = after - before

    return JSONResponse(response, status_code=status)


routes = [
    Route(f'/login/{super_user_url}', login_super_user, methods=['POST']),
    Route(f'/condominium/{super_user_url}', register_condominium_super_user, methods=['POST']),
    Route('/login/{login_type}', login, methods=['POST']),
    Route('/register/{registration_type}', register, methods=['POST']),
    Route('/employees', employees, methods=['GET']),
    Route('/residents', residents, methods=['GET']),
    Route('/notification/', notification, methods=['GET', 'POST', 'DELETE']),
    Route('/guest', guest, methods=['GET', 'POST', 'DELETE']),
    Route('/service', service, methods=['GET', 'POST', 'DELETE']),
    Route('/rule', rule, methods=['GET', 'POST', 'DELETE']),
    Route('/event_type', event_type, methods=['GET']),
    Route('/event', event, methods=['GET', 'POST', 'DELETE'])
]


middleware = [
    Middleware(CORSMiddleware, allow_origins=['*']),
    Middleware(SessionMiddleware, secret_key=secrets.token_urlsafe(37))
]

app = Starlette(routes=routes, middleware=middleware)
