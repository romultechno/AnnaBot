from aiogram import types, F, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.keyboards import kb1, kb2, kb3
import config
from API import gigachat2
from db_utils import db_commands

router = Router()

class question_feedback(StatesGroup):
    get_recommendation = State()
    #choice_feedback = State()



# Хэндлер на команду /start
@router.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    name = message.chat.first_name
    await message.answer(f'Привет, {name}', reply_markup=kb3)
    #await message.answer('Это мой учебный бот. Здесь реализованы простые фильтры и запрос к API нейросети Gigachat от Сбербанка')
    #await message.answer('Можно нажимать на кнопки и вводить произвольный текст', reply_markup=kb3)
    # ставим ловушку на обратную связь
    await state.set_state(question_feedback.get_recommendation)


@router.message(F.text.lower() == 'покажи совет')
async def cmd_recommendation(message: types.Message, state: FSMContext):

    question = db_commands.get_question_by_user_id(message.chat.id)

    if question.id > 0:
        # записываем номер выпавшего вопроса в состояние
        await state.update_data(question_id=question.id)
        # qtext = question.text
        await message.answer(str(question.id) + ' из ' + str(question.maximum))
        await message.answer(question.text)

        answertext = gigachat2.question_answer(config.preqtext + question.text)

        #await message.answer('Ответ по API:')
        await message.answer(answertext)
        await message.answer('Насколько совет актуален для Вас?', reply_markup=kb2)
    else:# если все вопросы в неактуальных
        await message.answer('У меня нет актуальных советов для Вас. Вы абсолютный гуру!', reply_markup=kb1)

    #ставим ловушку на обратную связь
    #await state.set_state(question_feedback.choice_feedback)


@router.message(F.text.lower() == 'ещё не задумывался')
async def cmd_neutral_feedback(message: types.Message, state: FSMContext):
    #await state.update_data(feedback=0)
    await message.answer('Значит время ещё не пришло. Подождём его вместе.',reply_markup=kb3)


@router.message(F.text.lower() == 'это интересно')
async def cmd_positive_feedback(message: types.Message, state: FSMContext):
    #await state.update_data(feedback=1)
    user_data = await state.get_data()
    # фиксируем проявление интереса
    await message.answer(f'Отработка позитивной обратной связи по {str(user_data.get("question_id"))}')
    db_commands.set_positive_feedback(message.chat.id, user_data.get("question_id"))
    await message.answer('Более подробно этот вопрос можно разобрать на курсе "Дамы с деньгами" или на личной консультации', reply_markup=kb3)


@router.message(F.text.lower() == 'я уже гуру')
async def cmd_negative_feedback(message: types.Message, state: FSMContext):
#    await state.update_data(feedback=-1)
    user_data = await state.get_data()
    # фиксируем отсутствие интереса
    await message.answer(f'Отработка негативной обратной связи по {str(user_data.get("question_id"))}')
    db_commands.set_negative_feedback(message.chat.id, user_data.get("question_id"))
    await message.answer('Я рада, что образованных людей в сфере финансов становится всё больше. Советов по этому вопросу Вам больше давать не буду.',reply_markup=kb3)



# Хендлер на сообщения
@router.message(F.text)
async def msg_echo(message: types.Message):
    msg_user = message.text.lower()
    name = message.chat.first_name
    await message.answer('Отработка ввода произвольного текста.')
    await message.answer('Введённое сообщение через API отправляется в нейросеть Gigachat')
    await message.answer('Ответ по API:')
    answertext = gigachat2.question_answer(msg_user)
    await message.answer(answertext, reply_markup=kb1)

# Хэндлер на команду /stop
@router.message(Command('stop'))
async def cmd_stop(message: types.Message):
        name = message.chat.first_name
        await message.answer(f'Пока, {name}')
