import re

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
                Inheritances.menu_id_ancestor.in_(args['menu_id']),
                and_(
                    Inheritances.menu_id_descendant.in_(args['menu_id']),
                    Inheritances.reversible == True
                )
            )
        )
    inhers = inhers.filter_by(active=True).all()

    if not inhers:
        return {}

    return inhers


def select_menu(args):
    menu_select = Menu.query
    if 'menu_ids' in args:
        menu_select = Menu.query.filter(Menu.id.in_(args['menu_ids']))
    if 'menu_names' in args:
        menu_select = Menu.query.filter(Menu.name.in_(args['menu_names']))
    if 'menu_authors' in args:
        menu_select = Menu.query.filter(Menu.author_id.in_(args['menu_authors']))

    try:
        menu = menu_select.filter_by(active=True).all()
    except Exception as e:
        abort(422, 'Something WRONG - {}'.format(e))

    if 'filled_text' in args:
        if args['filled_text'] == 'true':
            text_replace(menu)

    if not menu:
        return {}

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