import re
import operator
from pyaspeller import Word
import pymorphy2


correct_word = {'иксс', 'исит', 'гф', 'вуц', 'ртс', 'цэуби', 'ффп', 'ино', 'студак', 'оргком', 'васька', 'научка',
                'кнр', 'соц', 'студ', 'ксс', 'яковлевка', 'бончевские', 'соцотдел', 'бончёвские', 'купп', 'спбкт',
                'дальнике', '086у', 'стипуха', 'сис', 'wi-fi', 'ingut', 'альняк', 'кппк', 'bonch', 'оссо',
                'крит', 'вайфай', 'ингут', 'wifi', 'стипа', 'ссо', 'вифи'}

layout = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                           'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
                  "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                  'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))

values = {'инфокоммуникационых сети и системы': 'иксс',
          'радиотехнологий и связи': 'ртс',
          'информационных систем и технологий': 'исит',
          'военный учебный центр': 'вуц',
          'цифровой экономики управления и бизнес информатики': 'цэуби',
          'факультет фундаментальной подготовки': 'ффп',
          'фундаментальной подготовки': 'фп'}


def processing_user_request(word):
    """
    Для передаваймого слова исправляет опечатки и меняет раскладку, если она неправельная.
    И приводит к нормальной форме.
    :param word: не измененое слово
    :return: word or lemmatization(res.spellsafe): исправленое слово
    """
    translate_word = word.translate(layout)
    if word in correct_word:
        return word
    if translate_word in correct_word:
        return translate_word
    word = word.translate(layout)
    res = Word(word)
    if not res.correct and res.spellsafe is not None:
        return lemmatization(res.spellsafe)
    else:
        return word


def lemmatization(word):
    """
    Приводит слово к нормальной форме.
    :param word:
    :return: p.normal_form: приведеное к нормальной форме слово
    """
    morph = pymorphy2.MorphAnalyzer()
    p = morph.parse(word)[0]
    return p.normal_form


def dict_args(args: dict):
    """
    Возвращает слово переданое в парсере, не обращая внимания на знаки припинаия
    :param args:
    :return:
    """
    return {key: [value] for key, value in args.items()}


def replace_abbr(text):
    text = multiple_replace(text, values)
    return text


def multiple_replace(target_str, replace_values):
    for i, j in replace_values.items():
        target_str = target_str.replace(i, j)
    return target_str
