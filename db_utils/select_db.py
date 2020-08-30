import re
from flask import request, abort
from sqlalchemy import or_, and_

from db_utils.database import Menu, Attachment, Inheritances
from utils.request_utils import processing_user_request, replace_abbr
from utils.response_utils import smart_search


def select_attachment(args):
    attachment = Attachment.query
    if 'menu_id' in args:
        attachment = Attachment.query.filter(Attachment.menu_id.in_(args['menu_id']))
    attachment = attachment.all()

    if not attachment:
        return {}

    return attachment


def select_inheritances(args):
    inhers = Inheritances.query
    if 'menu_id' in args:
        inhers = Inheritances.query.filter(
            or_(
                Inheritances.menu_id_ancestor == args['menu_id'],
                and_(
                    Inheritances.menu_id_descendant == args['menu_id'],
                    Inheritances.reversible == 1
                )
            )
        )
    inhers = inhers.filter_by(active=True).all()

    if not inhers:
        return {}

    return inhers


def select_menu(args):
    menu = Menu.query.all()
    try:
        if 'menu_names' in args:
            menu = Menu.query.filter(Menu.name == args['menu_names']).all()
        if 'menu_ids' in args:
            menu = []
            for i in args['menu_ids']:
                menu.extend(Menu.query.filter(Menu.id == i).all())
    except Exception as e:
        print('Something WRONG - {}'.format(e))

    if 'filled_text' in args:
        if args['filled_text'] == 'true':
            text_replace(menu)

    return menu


def get_search(args):
    if 'text' in args:
        user_request = re.sub("[\".,«»()–:!?@\-]", ' ', args['text'][0].lower())
        user_request = user_request.lstrip().rstrip().strip()
        user_request = re.sub(r'\s+', ' ', user_request)
        user_request = replace_abbr(user_request).split(' ')
        res = [processing_user_request(word) for word in user_request]
        if 'ваня' in res:
            res.remove('ваня')
        res = smart_search(res)
        return res, 200
    else:
        return {}, 404
