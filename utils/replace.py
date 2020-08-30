import re
from itertools import chain

from db.db import Replace


def text_replace(filling_obj):
    """
    Заменяет переменные в тексте вида {example} на соостветсвующую переменную в бд.
    """
    all_text = ''

    for obj in filling_obj:
        all_text += obj.text

    names_arr = set(chain(re.findall('{\w+}', all_text)))
    names_arr = [key[1:-1] for key in names_arr]
    replace_arr = Replace.query.filter(Replace.name.in_(names_arr)).all()
    replace_obj = {replace.name: replace.value for replace in replace_arr}

    for obj in filling_obj:
        obj.text = obj.text.format(**replace_obj)

    return filling_obj
