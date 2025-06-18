from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup

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

