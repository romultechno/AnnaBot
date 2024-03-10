from aiogram import types


button1 = types.KeyboardButton(text='/start')
button2 = types.KeyboardButton(text='/stop')
button3 = types.KeyboardButton(text='Покажи совет')
button5 = types.KeyboardButton(text='Ещё не задумывался')
button6 = types.KeyboardButton(text='Это интересно')
button4 = types.KeyboardButton(text='Я уже гуру')

# start, stop, покажи совет
keyboard1 = [
    [button1, button2],
    [button3],
]

#обратная связь после советов
keyboard2 = [
    [button4],
    [button5],
    [button6],
]

#покажи совет
keyboard3 = [
    [button3],
]


kb1 = types.ReplyKeyboardMarkup(keyboard=keyboard1, resize_keyboard=True)
kb2 = types.ReplyKeyboardMarkup(keyboard=keyboard2, resize_keyboard=True)
kb3 = types.ReplyKeyboardMarkup(keyboard=keyboard3, resize_keyboard=True)