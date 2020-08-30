import vk_api
import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def send_message(session, peer_id, message=None, user_attachment=None, user_keyboard=None):
    """
    :type session: сессия вк устававлимая через токен
    :type peer_id: id пользователя
    :type message: сообщение для пользователя
    :type user_attachment: вложения для пользователя
    :type user_keyboard: клавиатура для пользователя
    """
    session.method('messages.send', {
        'peer_id': peer_id,
        'message': message,
        'random_id': random.randint(-2147483648, +2147483648),
        "attachment": user_attachment,
        'keyboard': user_keyboard
    })


def create_keyboard(name_arr, inline=False, one_time=True):
    """
    (len(name_arr_descendant) <= 10) - должно быть
    :param one_time: исчезает ли клавиатура после нажатия (по умолчанию исчезает)
    :param inline:  встроеная клавиатура в сообщение (по умолчанию нет)
    :type name_arr: массив названий кнопок потомков
    """
    user_keyboard = VkKeyboard(one_time=one_time, inline=inline)
    count = 0
    for name in name_arr:
        if count == 12:
            break
        count += 1
        user_keyboard.add_button(name, color=VkKeyboardColor.DEFAULT)
        if (count % 2 == 0) and (name != name_arr[-1]) and (count <= 10):
            user_keyboard.add_line()
    user_keyboard = user_keyboard.get_keyboard()
    return user_keyboard
