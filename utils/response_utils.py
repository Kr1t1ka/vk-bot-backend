import re

from db_utils.database import Menu
from utils.replace import text_replace


def smart_search(request_arr):
    """
    Получает обработаный запрос пользователя в виде массива, сопостовляет с тегами статей и подбирате наиболее
    подходящую статью.
    :param request_arr:
    :return: [<Menu>,...  ]
    """
    all_menu = Menu.query.all()
    index_lib_tags = {menu.id: str(menu.tags).split(' ') for menu in all_menu}
    index_lib_text = {menu.id: create_index(menu.text) for menu in all_menu}
    menu_rating = {menu.id: 0 for menu in all_menu}

    for menu in index_lib_tags:
        for word in request_arr:
            if word in index_lib_tags[menu]:
                menu_rating[menu] += 5 / len(index_lib_tags[menu])
            if word in index_lib_text[menu]:
                menu_rating[menu] += 2.5 / len(index_lib_tags[menu])

    res = [k for k, v in menu_rating.items() if v > 0]
    menu_arr = text_replace(Menu.query.filter(Menu.id.in_(res)).all())
    res = [{'menu': menu, 'rating': str(menu_rating[menu.id])} for menu in menu_arr]
    return res


def create_index(text):
    stopwords = {'в', 'и', 'с', 'на', 'при', 'об', 'не', 'по', 'со'}
    text = text.lower()
    text = re.sub("[\".,«»()–:!?@\d]", ' ', text)
    text = text.lstrip().rstrip().strip()
    text = [word for word in re.split("\W+", text) if word not in stopwords]
    return text
