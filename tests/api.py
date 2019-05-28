import requests

from config import BASE_URL


def _url(path):
    return BASE_URL + path


def get_user_message(username):
    return requests.get(_url(f'/hello/{username}'))


def healthcheck():
    return requests.get(_url('/healthcheck'))


def version():
    return requests.get(_url('/version'))


def put_user(username, birthdate):
    user = {"dateOfBirth": birthdate}
    return requests.put(_url(f'/hello/{username}'), json=user)
