import sqlite3
import warnings
import config
import random

class Question:
    def __init__(self, id, text, maximum):
        self.id = id
        self.text = text
        self.maximum = maximum

warnings.simplefilter("ignore", DeprecationWarning)

#conn_themes = sqlite3.connect(config.themes_path)
#conn = sqlite3.connect(config.db_path)
#c = conn.cursor()
#ct = conn_themes.cursor()

#создание (в случае отсутствия) базы данных с актуальностью вопросов для пользователей
def initialize_db(db_path):
    conn = sqlite3.connect(config.db_path)
    c = conn.cursor()

    #актуальные вопросы
    c.execute('''CREATE TABLE IF NOT EXISTS user_relevant_questions (
        user_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        is_relevant BOOLEAN NOT NULL,
        PRIMARY KEY (user_id, question_id),
        FOREIGN KEY (question_id) REFERENCES questions (id)
    )''')
    conn.commit()

    #актуальные темы
    c.execute('''CREATE TABLE IF NOT EXISTS user_relevant_themes (
        user_id INTEGER NOT NULL,
        theme_id INTEGER NOT NULL,
        is_relevant BOOLEAN NOT NULL,
        PRIMARY KEY (user_id, theme_id),
        FOREIGN KEY (theme_id) REFERENCES themes (id)
    )''')
    conn.commit()

    #не актуальные вопросы (уже гуру)
    c.execute('''CREATE TABLE IF NOT EXISTS user_not_relevant_questions (
        user_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        is_not_relevant BOOLEAN NOT NULL,
        PRIMARY KEY (user_id, question_id),
        FOREIGN KEY (question_id) REFERENCES not_relevant_questions (id)
    )''')
    conn.commit()
    conn.close()

# Вспомогательные функции
#получить id неактуальных вопросов
def get_not_relevant_questions (user_id):
    conn = sqlite3.connect(config.db_path)
    c = conn.cursor()

    # Запрос к базе данных для получения всех question_id, где is_not_relevant = True для данного user_id
    c.execute('SELECT question_id '
              'FROM user_not_relevant_questions '
              'WHERE '
                 'user_id = ? AND '
                 'is_not_relevant = ?', (user_id, True))
    not_relevant_questions = [row[0] for row in c.fetchall()]

    conn.close()

    return not_relevant_questions


#получить список id возможных вопросов
def get_possible_questions(not_relevant_questions):
    conn_themes = sqlite3.connect(config.themes_path)
    c = conn_themes.cursor()

    # Запрос к базе данных для получения всех question_id, где is_not_relevant = True для данного user_id
    c.execute('SELECT id '
              'FROM questions')
    all_possible_questions = [row[0] for row in c.fetchall()]
    #сравнение массивов. отсавляем только такие вопросы, которые не помечены как неактуальные
    possible_questions = [question for question in all_possible_questions if question not in not_relevant_questions]

    conn_themes.close()

    return possible_questions

def get_question_text_by_id(question_id):
    conn_themes = sqlite3.connect(config.themes_path)
    c = conn_themes.cursor()
    c.execute('SELECT question FROM questions WHERE id = ?', (question_id,))
    question = c.fetchone()
    conn_themes.close()
    if question:
        return question[0]
    else:
        return 'У меня нет актуальных советов для Вас'

# получить текст вопроса
def get_question(possible_questions):

    question_text = ''
    question_capacity = len(possible_questions)
    if question_capacity > 0:
        question_id = random.choice(possible_questions)
        question_text = get_question_text_by_id(question_id)
        question = Question(question_id, question_text, question_capacity)
    else:
        question = Question(0, '', 0)

    return question

def get_question_by_user_id(user_id):
    question = get_question(get_possible_questions(get_not_relevant_questions(user_id)))

    #question_text = get_question_text(get_possible_questions(get_not_relevant_questions(user_id)))
    return question

def set_negative_feedback(user_id,question_id):
    conn = sqlite3.connect(config.db_path)
    c = conn.cursor()

    c.execute("INSERT INTO user_not_relevant_questions (user_id, question_id, is_not_relevant) VALUES (?, ?, ?)",
              (user_id, question_id, True))
    conn.commit()

    conn.close()


def set_positive_feedback(user_id,question_id):
    conn = sqlite3.connect(config.db_path)
    c = conn.cursor()

    c.execute("INSERT INTO user_relevant_questions (user_id, question_id, is_relevant) VALUES (?, ?, ?)",
              (user_id, question_id, True))
    conn.commit()

    conn.close()


# def get_topic_id_by_question(question):
#     c.execute('SELECT topic_id FROM questions WHERE question = ?', (question,))
#     result = c.fetchone()
#     return result[0] if result else None
#
# def get_relevant_questions(user_id):
#     c.execute('''
#         SELECT q.question, t.name FROM questions q
#         JOIN topics t ON q.topic_id = t.id
#         JOIN user_topics ut ON q.topic_id = ut.topic_id
#         WHERE ut.user_id = ? AND ut.is_relevant = 1
#     ''', (user_id,))
#     return c.fetchall()
#
# def update_user_topic_relevance(user_id, topic_id, is_relevant):
#     c.execute('''
#         INSERT INTO user_topics (user_id, topic_id, is_relevant)
#         VALUES (?, ?, ?)
#         ON CONFLICT(user_id, topic_id) DO UPDATE SET is_relevant = excluded.is_relevant
#     ''', (user_id, topic_id, is_relevant))
#     conn.commit()

