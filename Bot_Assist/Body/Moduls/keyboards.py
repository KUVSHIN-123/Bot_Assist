from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup


ikb1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Завершить',callback_data='complete')]
])

ikb2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мои задания',callback_data='my tasks')]
])

ikb3 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Посмотреть задания',callback_data='check tasks'),
     InlineKeyboardButton(text='Дать задания',callback_data='give tasks')]
])

ikb4 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Данные верны',callback_data='data accept'),
     InlineKeyboardButton(text='Данные неверны',callback_data='data incorrect')]
])

ikb5 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтвердить',callback_data="accept"),
     InlineKeyboardButton(text='Изменить',callback_data="edit")]
])

ikb6 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтвердить отправку',callback_data="sending accept"),
     InlineKeyboardButton(text='Отменить отправку',callback_data="cancel sending")]
])

# ФУНКЦИЯ ДЛЯ СБОРКИ СПИСКА ЗАДАНИЙ
def builder_list_tasks(id_task):
    keyboard = []
    keyboard.append([InlineKeyboardButton(text='Завершить',callback_data=f'{id_task}')])
    ikb7 = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return ikb7

# ФУНКЦИЯ ДЛЯ СБОРКИ СПИСКА ПОЛЬЗОВАТЕЛЕЙ
def builder_list_users(list_users):
    keyboard = []
    for i in list_users:
        keyboard.append([InlineKeyboardButton(text=f'{i[1]} {i[2]}',callback_data=f'{i[0]}')])
    ikb8 = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return ikb8
