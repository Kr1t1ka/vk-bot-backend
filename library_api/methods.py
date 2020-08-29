import requests
import time
from app.connection import library_api


def get_menu(menu_ids=None, menu_names=None, menu_authors=None, filled_text=True):
    i = 0
    if isinstance(menu_ids, list):
        menu_ids = create_params(menu_ids)
    if isinstance(menu_names, list):
        menu_names = create_params(menu_names)

    params = {'menu_ids': menu_ids, 'menu_names': menu_names, 'menu_authors': menu_authors, 'filled_text': filled_text}
    while i < 20:
        try:
            return requests.get(library_api + '/menu/', params=params).json()
        except:
            i += 1
            time.sleep(1)
    print('Error: 500')


def get_inheritances(menu_id=None):
    i = 0
    params = {'menu_id': menu_id}
    while i < 20:
        try:
            return requests.get(library_api + '/inheritances/', params=params).json()
        except:
            i += 1
            time.sleep(1)
    print('Error: 500')


def get_search(text):
    i = 0
    params = {'text': text}
    while i < 20:
        try:
            return requests.get(library_api + '/search/', params=params).json()
        except:
            i += 1
            time.sleep(1)
    print('Error: 500')


def create_params(arr):
    params = ''
    for obj in arr:
        params += str(obj) + ','
    return params[0:-1]
