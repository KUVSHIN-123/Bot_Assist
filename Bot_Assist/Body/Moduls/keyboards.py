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
    [InlineKeyboardButton(text='Подтвердить задание',callback_data="task accept"),
     InlineKeyboardButton(text='Переписать задание',callback_data="task rewrite")]
])

ikb6 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтвердить ',callback_data="accept"),
     InlineKeyboardButton(text='Изменить ',callback_data="edit")]
])

ikb7 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтвердить выбор',callback_data="choice accept"),
     InlineKeyboardButton(text='Изменить выбор',callback_data="choice edit")]
])

ikb8 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтвердить отправку',callback_data="sending accept"),
     InlineKeyboardButton(text='Отменить отправку',callback_data="cancel sending")]
])